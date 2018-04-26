from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app.dashboard import bp
from app.dashboard.forms import RegistrationForm, EditProfileForm
from app.models import User
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
    user = User.query.filter_by(username=current_user.username).first_or_404()
    return render_template(
        'dashboard/overview.html', user=user, title='Dashboard')


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
    return render_template(
        'dashboard/add_user.html', title='Add User', form=form)


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
                           form=form)
