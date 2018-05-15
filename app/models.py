from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from hashlib import md5
from app import db, login
from time import time
import jwt
from flask import current_app

# the post-tag association table (many-to-many)
post_tag = db.Table('post_tag',
                    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
                    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
                    )


class User(UserMixin, db.Model):
    # register
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    post = db.relationship('Post', backref='author', lazy='dynamic')
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    # profile edit & register
    about_me = db.Column(db.String(280))
    screen_name = db.Column(db.String(64), index=True)
    website = db.Column(db.String(280), index=True)
    github = db.Column(db.String(280), index=True)
    twitter = db.Column(db.String(280), index=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        # creates a password hash to be stored in the db
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        # compares the password and the hash
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(280), index=True, unique=True)
    body = db.Column(db.String())
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # many-to-many tags-posts
    tag = db.relationship('Tag', secondary=post_tag,
                          backref=db.backref('posts', lazy='dynamic'),
                          lazy='dynamic')

    def __repr__(self):
        return 'Post ({})'.format(self.title)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), index=True, unique=True)

    @staticmethod
    def check_new_tag(tag):
        return Tag.query.filter_by(name=tag).first()

    @staticmethod
    def add_existing_tag(post, ex_tag):
        post.tag.append(ex_tag)

    def __repr__(self):
        return '{}'.format(self.name)


@login.user_loader
def load_user(id):
    """
    Each time the logged-in user navigates to a new page, Flask-Login
    retrieves the ID of the user from the session, and then loads that
    user into memory.
    """
    return User.query.get(int(id))
