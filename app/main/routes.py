from flask import render_template, url_for
from flask_login import login_required, current_user
from app.main import bp
from app.models import User, Post


@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html', title='Home')


@bp.route('/blog')
def blog():
    all_posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('blog.html', title='Blog', all_posts=all_posts)


@bp.route('/about')
def about():
    return render_template('about.html', title='About')


@bp.route('/author/<username>')
def author(username):
    user = User.query.filter_by(username=username).first_or_404()
    author = 'About {}'.format(user.username)
    my_posts = Post.query.filter_by(
        user_id=user.id).order_by(Post.timestamp.desc())
    return render_template(
        'author.html', user=user, my_posts=my_posts, title=author)
