from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app.dashboard import bp
from app.dashboard.forms import RegistrationForm, EditProfileForm, PostForm
from app.models import User, Post
from app import db
from datetime import datetime


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@bp.route('/overview')
@login_required
def overview():
    user = User.query.filter_by(username=current_user.username).first()
    my_posts = Post.query.filter_by(
        user_id=current_user.id).order_by(Post.timestamp.desc())
    return render_template('dashboard/overview.html', user=user,
                           title='Dashboard', my_posts=my_posts,
                           dashboard_active='is-active',
                           overview_active='is-active')


@bp.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('User {} has been Added.'.format(form.username.data))
    return render_template('dashboard/add_user.html', title='Add User',
                           form=form, dashboard_active='is-active',
                           add_active='is-active')


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        current_user.email = form.email.data
        current_user.screen_name = form.screen_name.data
        current_user.website = form.website.data
        current_user.github = form.github.data
        current_user.twitter = form.twitter.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('dashboard.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
        form.email.data = current_user.email
        form.screen_name.data = current_user.screen_name
        form.website.data = current_user.website
        form.github.data = current_user.github
        form.twitter.data = current_user.twitter
    return render_template('dashboard/edit_profile.html', title='Edit Profile',
                           form=form, dashboard_active='is-active',
                           edit_active='is-active')


@bp.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user,
                    title=form.title.data)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('dashboard.overview'))
    return render_template('dashboard/new_post.html', title='New Post',
                           form=form, dashboard_active='is-active',
                           post_active='is-active')


@bp.route('/edit_post/<id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Post.query.filter_by(id=id).first_or_404()
    form = PostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.post.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('dashboard.overview'))
    elif request.method == 'GET':
        form.title.data = post.title
        form.post.data = post.body

    return render_template('dashboard/edit_post.html', post=post, form=form,
                           title='Edit Post', dashboard_active='is-active',
                           overview_active='is-active')


@bp.route('/delete_post/<id>', methods=['POST'])
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first_or_404()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('auth.login'))
