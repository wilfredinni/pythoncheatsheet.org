from flask import render_template, url_for, request, current_app
from flask_login import login_required, current_user
from app.main import bp
from app.models import User, Post, Tag
import requests
import mistune
import json


def markdown(text):
    '''
    parse markdown to html
    '''
    md = mistune.Markdown()
    return md(text)


@bp.route('/')
@bp.route('/index')
def index():
    index_r = requests.get(current_app.config['INDEX_URL'])
    index = markdown(index_r.text)

    pysheet_r = requests.get(current_app.config['PYSHEET_URL'])
    pysheet = markdown(pysheet_r.text)
    return render_template('main/index.html', title='Home',
                           index=index, pysheet=pysheet)


@bp.route('/blog')
def blog():
    # pass the markdown converter to the template (only here)
    md = mistune.Markdown()
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
                           next_url=next_url, prev_url=prev_url, md=md)


@bp.route('/blog/tag/<tag>')
def tag(tag):
    md = mistune.Markdown()
    tag = Tag.query.filter_by(name=tag).first()
    posts = tag.posts.order_by(Post.timestamp.desc())
    return render_template('main/tag_articles.html', title='Tag', tag=tag,
                           posts=posts, md=md)


@bp.route('/article/<id>')
def article(id):
    post = Post.query.filter_by(id=id).first_or_404()
    # parse the markdown to html
    body = markdown(post.body)
    return render_template('main/article.html', post_body=body, post=post,
                           title=post.title)


@bp.route('/contribute')
def contribute():
    contribute_r = requests.get(current_app.config['CONTRIBUTING'])
    contribute = markdown(contribute_r.text)
    return render_template('main/contribute.html', title="Contribute",
                           contribute_md=contribute)


@bp.route('/about')
def about():
    about_r = requests.get(current_app.config['ABOUT'])
    about = markdown(about_r.text)
    return render_template('main/about.html', title='About', about_md=about)


@bp.route('/author/<username>')
def author(username):
    user = User.query.filter_by(username=username).first_or_404()
    if user.about_me:
        about_me = markdown(user.about_me)
    else:
        about_me = ""
    author = f'About {user.username}'
    my_posts = Post.query.filter_by(
        user_id=user.id).order_by(Post.timestamp.desc())
    return render_template('main/author.html', user=user, my_posts=my_posts,
                           title=author, about_me=about_me)
