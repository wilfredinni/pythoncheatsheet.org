from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from hashlib import md5
from app import db, login


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


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(280), index=True, unique=True)
    body = db.Column(db.String())
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return 'Post({})'.format(self.title)


@login.user_loader
def load_user(id):
    """
    Each time the logged-in user navigates to a new page, Flask-Login
    retrieves the ID of the user from the session, and then loads that
    user into memory.
    """
    return User.query.get(int(id))
