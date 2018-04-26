from flask import render_template, url_for
from flask_login import login_required, current_user
from app.main import bp
from app.models import User


@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html', title='Home')


@bp.route('/blog')
def blog():
    return render_template('blog.html', title='Blog')


@bp.route('/about')
def about():
    return render_template('about.html', title='About')


@bp.route('/author/<username>')
def author(username):
    user = User.query.filter_by(username=username).first_or_404()
    author = 'About {}'.format(user.username)
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('author.html', user=user, posts=posts, title=author)
