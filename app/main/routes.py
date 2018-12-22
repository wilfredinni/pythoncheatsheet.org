from flask import render_template, url_for, request, current_app, redirect, \
    send_from_directory
from app.main import bp
from app.models import User, Post, Tag, PinedMsg
import requests
import mistune
from flask import g
from app.main.froms import SearchForm


@bp.before_app_request
def before_request():

    g.search_form = SearchForm()
    g.search_switch = current_app.config["SEARCH_SWITCH"]
    g.site_name = current_app.config["SITE_NAME"]
    g.md = mistune.Markdown()  # parse md to html
    g.all_tags = Tag.query.all()


@bp.route('/index')
@bp.route('/')
def index():

    # get the cheatsheet form the repository
    pysheet = requests.get(current_app.config['PYSHEET_URL']).text

    # get the pinned msg and check if its enabled
    pinned_msg = PinedMsg.query.filter_by(id=1).first()

    return render_template('main/index.html',
                           pysheet=pysheet,
                           title='Python Cheatsheet',
                           pinned_msg=pinned_msg)


@bp.route('/blog')
def blog():

    # all posts
    posts = Post.query.all()

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
                           next_url=next_url, prev_url=prev_url,
                           blog_posts=posts)


@bp.route('/blog/tag/<tag>')
def tag(tag):

    tag = Tag.query.filter_by(name=tag).first()
    posts = tag.posts.order_by(Post.timestamp.desc())
    title = 'Tag: {}'.format(tag.name)

    return render_template('main/tag_articles.html', title=title, tag=tag,
                           posts=posts)


@bp.route('/blog/<url>')
def article(url):

    post = Post.query.filter_by(url=url).first_or_404()
    body = requests.get(post.markdown_url).text
    is_article = True

    return render_template('main/article.html', post=post, title=post.title,
                           md_body=body, is_article=is_article)


@bp.route('/contribute')
def contribute():

    contribute_r = requests.get(current_app.config['CONTRIBUTING'])
    contribute = contribute_r.text

    return render_template('main/md_pages.html', title="Contribute",
                           md_render=contribute)


@bp.route('/about')
def about():

    about_r = requests.get(current_app.config['ABOUT'])
    about = about_r.text

    return render_template('main/md_pages.html', title='About',
                           md_render=about)


@bp.route('/author/<username>')
def author(username):

    user = User.query.filter_by(username=username).first_or_404()

    if user.about_me:
        about_me = user.about_me
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

    page = request.args.get('page', 1, type=int)

    posts, total = Post.search(g.search_form.q.data, page,
                               current_app.config['POSTS_PER_PAGE'])

    return render_template('main/search.html', title='Search', posts=posts,
                           total=total)


@bp.route('/tags')
def tags():
    all_tags = Tag.query.all()

    return render_template('main/tags.html', title="Tags", all_tags=all_tags)


@bp.route('/sitemap.xml')
def sitemap():

    return send_from_directory('static', filename='sitemap.xml')


@bp.route('/robots.txt')
def robot():

    return send_from_directory('static', filename='robots.txt')


@bp.route('/BingSiteAuth.xml')
def bing():

    return send_from_directory('static', filename='BingSiteAuth.xml')


@bp.route('/.well-known/acme-challenge/TRcOHURRJJEDaaas6wgHsP232DQaqY0HnHvadMU-SMY')
def acme1():

    return send_from_directory('static/.well-known/acme-challenge', filename='TRcOHURRJJEDaaas6wgHsP232DQaqY0HnHvadMU-SMY')


@bp.route('/.well-known/acme-challenge/zO6V6tGs5eWBqa77cRt_oaS9osezokFNHd_YNThG5sU')
def acme2():

    return send_from_directory('static/.well-known/acme-challenge', filename='zO6V6tGs5eWBqa77cRt_oaS9osezokFNHd_YNThG5sU')
