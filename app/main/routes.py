from flask import render_template, url_for, request, current_app
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
    # pagination
    page = request.args.get('page', 1, type=int)
    all_posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'])
    # get the next page url
    next_url = url_for('main.blog', page=all_posts.next_num) \
        if all_posts.has_next else None
    # get the previous page url
    prev_url = url_for('main.blog', page=all_posts.prev_num) \
        if all_posts.has_prev else None
    return render_template('main/blog.html', title='Blog', all_posts=all_posts,
                           blog_active='is-active', next_url=next_url,
                           prev_url=prev_url)


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
    author = f'About {user.username}'
    my_posts = Post.query.filter_by(
        user_id=user.id).order_by(Post.timestamp.desc())
    return render_template('main/author.html', user=user, my_posts=my_posts,
                           title=author, profile_active='is-active')
