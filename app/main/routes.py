from flask import render_template, url_for
from flask_login import login_required, current_user
from app.main import bp
from app.models import User, Post


@bp.route('/')
@bp.route('/index')
def index():
    return render_template('main/index.html', title='Home',
                           home_active='is-active')


@bp.route('/blog')
def blog():
    all_posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('main/blog.html', title='Blog', all_posts=all_posts,
                           blog_active='is-active')


@bp.route('/article/<id>')
def article(id):
    post = Post.query.filter_by(id=id).first_or_404()
    return render_template('main/article.html', post=post, title=post.title)


@bp.route('/about')
def about():
    return render_template('main/about.html', title='About',
                           about_active='is-active')


@bp.route('/author/<username>')
def author(username):
    user = User.query.filter_by(username=username).first_or_404()
    author = 'About {}'.format(user.username)
    my_posts = Post.query.filter_by(
        user_id=user.id).order_by(Post.timestamp.desc())
    return render_template('main/author.html', user=user, my_posts=my_posts,
                           title=author, profile_active='is-active')
