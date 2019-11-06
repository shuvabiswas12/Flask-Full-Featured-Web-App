from flask import Blueprint, redirect, flash, render_template, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from App import db, bcrypt
from App.models import User, Post

# for multiple lines I use parenthesis here for break the big line to multiple line
from App.users.forms import (RegistrationForm, LoginForm, ResetPasswordForm,
                             UpdateAccountForm, RequestResetForm)

from App.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('main./home')

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to login ', 'success')
        return redirect('/login')
    return render_template("register.html", title='Register', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/home')

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/home')
        else:
            flash("Login Unsuccessful. Please, check email and password!", 'danger')
    return render_template("login.html", title='Login', form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect('/home')


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            print('filename: ', picture_file)

            # save the picture name/info to database
            current_user.img_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data

        db.session.commit()

        flash("Your account has been updated!", 'success')
        return redirect(url_for('users.account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='css/profile_pic/' + current_user.img_file)
    print(image_file)

    return render_template('account.html', title='Account', image_file=image_file, form=form)


@users.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post().query.filter_by(author=user) \
        .order_by(Post.date_posted.desc()) \
        .paginate(page=page, per_page=4)
    return render_template("user_posts.html", posts=posts, title='User Posts', user=user)


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been send with instruction to reset password', 'info')
        return redirect(url_for('login'))
    return render_template("reset_request.html", title='Reset Password', form=form)


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.varify_reset_token(token)
    if user is None:
        flash("That is an invalid token", 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! ', 'success')
        return redirect('/login')

    return render_template('reset_token.html', form=form, title='Reset Password')
