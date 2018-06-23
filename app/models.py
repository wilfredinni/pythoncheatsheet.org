from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from hashlib import md5
from app import db, login
from time import time
import jwt
from flask import current_app
from app.search import add_to_index, remove_from_index, query_index


class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)


db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)

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
    is_administrator = db.Column(db.Boolean(), index=True, default=False)

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


class Post(SearchableMixin, db.Model):
    __searchable__ = ['title', 'body']
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(280), index=True, unique=True)
    url = db.Column(db.String(280), index=True, unique=True)
    body = db.Column(db.String(8000))
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

    @staticmethod
    def create_new_tag(tag, post):
        new_tag = Tag(name=tag)
        db.session.add(new_tag)
        post.tag.append(new_tag)

    @staticmethod
    def add_or_create_tags(post_tags, post):
        for tag in post_tags:
            # check if the tag exists and append it to the new post
            if Tag.query.filter_by(name=tag).first():
                ex_tag = Tag.query.filter_by(name=tag).first()
                Tag.add_existing_tag(post=post, ex_tag=ex_tag)
            else:
                # else, create it
                Tag.create_new_tag(tag, post)

    @staticmethod
    def check_deleted_tags(post, post_tags):
        # convert both list to sets and get the difference
        post_tags = set(post_tags)
        post_db_tags = set(post.tag.all())
        deleted_tags = list(post_db_tags.difference(post_tags))
        # remove the deleted tags from the post
        for tag in deleted_tags:
            post.tag.remove(tag)

    @staticmethod
    def update_tags(post_tags, post):
        for tag in post_tags:
            # check in the tags table
            t = Tag.check_new_tag(tag)
            if t:  # if there is a coincidence check if is appended to the post
                if t in post.tag.all():  # if is appended, pass
                    pass
                else:  # else, append it
                    Tag.add_existing_tag(
                        post=post, ex_tag=Tag.check_new_tag(tag))
            else:
                # else, create it
                Tag.create_new_tag(tag, post)

    def __repr__(self):
        return '{}'.format(self.name)


class PinedMsg(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    home_msg = db.Column(db.String(4000))
    home_enable = db.Column(db.Boolean(), index=True, default=False)


@login.user_loader
def load_user(id):
    """
    Each time the logged-in user navigates to a new page, Flask-Login
    retrieves the ID of the user from the session, and then loads that
    user into memory.
    """
    return User.query.get(int(id))
