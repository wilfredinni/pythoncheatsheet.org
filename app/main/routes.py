from flask import render_template, url_for, request, current_app, redirect
from flask_login import login_required, current_user
from app.main import bp
from app.models import User, Post, Tag, PinedMsg
import requests
import mistune
import json
from flask import g
from app.main.froms import SearchForm


@bp.before_app_request
def before_request():
    g.search_form = SearchForm()
    g.search_switch = current_app.config["SEARCH_SWITCH"]
    g.site_name = current_app.config["SITE_NAME"]
    g.md = mistune.Markdown()


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

    # get the pinned msg and check if its enabled
    pinned_msg = PinedMsg.query.filter_by(id=1).first()

    return render_template('main/index.html', title='Home',
                           index=index, pysheet=pysheet,
                           pinned_msg=pinned_msg)


@bp.route('/blog')
def blog():
    # pagination
    page = request.args.get('page', 1, type=int)
    all_posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'])
    # all posts
    posts = Post.query.all()
    # get the next page url
    next_url = url_for('main.blog', page=all_posts.next_num) \
        if all_posts.has_next else None
    # get the previous page url
    prev_url = url_for('main.blog', page=all_posts.prev_num) \
        if all_posts.has_prev else None
    return render_template('main/blog.html', title='Blog', all_posts=all_posts,
                           next_url=next_url, prev_url=prev_url,
                           blog_posts=posts)


@bp.route('/blog/tag/<tag>')
def tag(tag):
    tag = Tag.query.filter_by(name=tag).first()
    posts = tag.posts.order_by(Post.timestamp.desc())
    return render_template('main/tag_articles.html', title='Tag', tag=tag,
                           posts=posts)


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
    return render_template('main/md_pages.html', title="Contribute",
                           md_render=contribute)


@bp.route('/about')
def about():
    about_r = requests.get(current_app.config['ABOUT'])
    about = markdown(about_r.text)
    return render_template('main/md_pages.html', title='About',
                           md_render=about)


@bp.route('/author/<username>')
def author(username):
    user = User.query.filter_by(username=username).first_or_404()
    if user.about_me:
        about_me = markdown(user.about_me)
    else:
        about_me = ""
    if user.screen_name:
        author = 'About {}'.format(user.screen_name)
    else:
        author = 'About {}'.format(user.username)
    my_posts = Post.query.filter_by(
        user_id=user.id).order_by(Post.timestamp.desc())
    return render_template('main/author.html', user=user, my_posts=my_posts,
                           title=author, about_me=about_me)


@bp.route('/search')
def search():
    if not g.search_form.validate():
        return redirect(url_for('main.blog'))
    md = mistune.Markdown()
    page = request.args.get('page', 1, type=int)
    posts, total = Post.search(g.search_form.q.data, page,
                               current_app.config['POSTS_PER_PAGE'])

    return render_template('main/search.html', title='Search', posts=posts,
                           total=total, md=md)
