from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app.auth.forms import LoginForm, RegistrationForm
from werkzeug.urls import url_parse
from app.models import User
from app.auth import bp
from app import db


@bp.route('/login', methods=['GET', 'POST'])
def login():
    # prevent the logged user to navigates to the /login URL
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.overview'))
    form = LoginForm()
    if form.validate_on_submit():
        # load the user from the db
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        # register the user as logged in
        login_user(user, remember=form.remember_me.data)
        # redirect to the previous page or dashbord if not
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('dashboard.overview')
        return redirect(next_page)
    return render_template('auth/login.html', title='Login', form=form)


@bp.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    # prevent the logged user to navigates to the /register URL
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('User {} has been registered.'.format(form.username.data))
    return render_template('auth/register.html', title='Register', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
