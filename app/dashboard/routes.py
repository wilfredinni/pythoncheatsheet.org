from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app.dashboard import bp
from app.dashboard.forms import RegistrationForm, EditProfileForm, PostForm, \
    PinMsgForm
from app.models import User, Post, Tag, PinedMsg
from app import db
import re
from datetime import datetime


@bp.before_request
def before_request():
    # save the las activity of the user
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@bp.route('/overview')
@login_required
def overview():
    # for avatar and user name in the dashboard
    user = User.query.filter_by(username=current_user.username).first()
    my_posts = Post.query.filter_by(
        user_id=current_user.id).order_by(Post.timestamp.desc())
    # cant use my post to check if there are articles or not,
    # have to use this query:
    posts = Post.query.filter_by(user_id=current_user.id).first()
    return render_template('dashboard/overview.html', title='Dashboard',
                           my_posts=my_posts, overview_active='is-active',
                           user=user, post_list=posts)


@bp.route('/manage_articles')
@login_required
def manage_articles():
    # all posts ordered by date
    posts_list = Post.query.first()

    posts = Post.query.filter_by().order_by(Post.timestamp.desc())
    return render_template('dashboard/overview.html',
                           title='Manage Articles', my_posts=posts,
                           articles_active='is-active', post_list=posts_list)


@bp.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    form = RegistrationForm()
    if form.validate_on_submit():
        # if administrator check box is selected, create an administrator
        if form.administrator.data:
            user = User(username=form.username.data, email=form.email.data,
                        is_administrator=True)
        else:
            user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created for {}.'.format(form.username.data))
        return redirect(url_for('dashboard.manage_users'))
    return render_template('dashboard/add_user.html', title='Add User',
                           form=form, add_active='is-active')


@bp.route('/manage_users')
@login_required
def manage_users():
    all_users = User.query.all()
    return render_template('dashboard/manage_users.html', title='Manage Users',
                           all_users=all_users, users_active='is-active')


@bp.route('/edit_profile/<username>', methods=['GET', 'POST'])
@login_required
def edit_profile(username):
    if current_user.username != username:
        flash("You can't edit other users profiles.")
        return redirect(url_for('dashboard.overview'))
    user = User.query.filter_by(username=username).first_or_404()
    form = EditProfileForm(user.username)
    if form.validate_on_submit():
        user.username = form.username.data
        user.about_me = form.about_me.data
        user.email = form.email.data
        user.screen_name = form.screen_name.data
        user.website = form.website.data
        user.github = form.github.data
        user.twitter = form.twitter.data
        db.session.commit()
        flash('{}, your changes have been saved.'.format(form.username.data))
        return redirect(url_for('dashboard.overview'))
    elif request.method == 'GET':
        form.username.data = user.username
        form.about_me.data = user.about_me
        form.email.data = user.email
        form.screen_name.data = user.screen_name
        form.website.data = user.website
        form.github.data = user.github
        form.twitter.data = user.twitter

    return render_template('dashboard/edit_profile.html', form=form,
                           user=user, title='Edit Profile',
                           edit_active='is-active')


@bp.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(markdown_url=form.markdown_url.data, author=current_user,
                    title=form.title.data, url=form.url.data,
                    img_url=form.img_url.data, summary=form.summary.data)
        # split the tags by the comas
        post_tags = form.tags.data.replace(' ', '').split(',')

        # check if the tag exists to append it to the post. Else, create it
        Tag.add_or_create_tags(post_tags, post)
        # add tag and post
        db.session.add(post)
        # commit to the db
        db.session.commit()
        flash('"{}" is now live!'.format(form.title.data))
        return redirect(url_for('dashboard.overview'))
    return render_template('dashboard/new_post.html', title='New Post',
                           form=form, post_active='is-active')


@bp.route('/edit_post/<url>', methods=['GET', 'POST'])
@login_required
def edit_post(url):
    post = Post.query.filter_by(url=url).first_or_404()
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.url = form.url.data
        post.markdown_url = form.markdown_url.data
        post.summary = form.summary.data
        post.img_url = form.img_url.data

        # split the tags by comas
        post_tags = form.tags.data.replace(' ', '').split(',')

        # check for deleted tags
        Tag.check_deleted_tags(post, post_tags)

        # check for existing tags
        Tag.update_tags(post_tags, post)

        db.session.commit()
        flash('Changes on "{}" have been saved.'.format(form.title.data))
        return redirect(url_for('dashboard.overview'))
    elif request.method == 'GET':
        form.title.data = post.title
        form.url.data = post.url
        form.markdown_url.data = post.markdown_url
        form.summary.data = post.summary
        form.img_url.data = post.img_url
        # use regex to format the tags
        tag_regex = re.compile(r'\[(.*)\]')
        mo = tag_regex.search(str(post.tag.all()))
        form.tags.data = mo.group(1)

    return render_template('dashboard/new_post.html', post=post, form=form,
                           title='Edit Post', overview_active='is-active')


@bp.route('/site_configuration', methods=['GET', 'POST'])
@login_required
def site_configuration():
    form = PinMsgForm()
    msg = PinedMsg.query.filter_by(id=1).first()

    if form.validate_on_submit():
        if msg:
            msg.home_msg = form.home_msg.data
            msg.home_enable = form.home_enable.data
        else:
            msg = PinedMsg(home_msg=form.home_msg.data,
                           home_enable=form.home_enable.data)
            db.session.add(msg)
        db.session.commit()
        flash('The Pinned message has ben Updated.')
        return redirect(url_for('dashboard.site_configuration'))
    # check if there is a msg created and get it
    elif request.method == 'GET':
        if msg:
            form.home_msg.data = msg.home_msg
            if msg.home_enable:
                enabled = True
            else:
                enabled = False
        else:
            enabled = "None"
    return render_template('dashboard/site_configuration.html',
                           title='Site Configuration', form=form,
                           config_active='is-active', enabled=enabled)


@bp.route('/delete_user/<id>', methods=['POST'])
@login_required
def delete_user(id):
    user = User.query.filter_by(id=id).first_or_404()
    db.session.delete(user)
    db.session.commit()
    flash('User {} has been Deleted'.format(user.username))
    return redirect(url_for('dashboard.manage_users'))


@bp.route('/delete_post/<url>', methods=['GET', 'POST'])
@login_required
def delete_post(url):
    post = Post.query.filter_by(url=url).first_or_404()
    db.session.delete(post)
    db.session.commit()
    flash('"{}" has been Deleted'.format(post.title))
    return redirect(url_for('dashboard.overview'))
