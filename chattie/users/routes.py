from chattie import bcrypt, db, mail
from chattie.models import Profile, User
from chattie.users.forms import (ChangePasswordForm, EditUserProfile,
                                 LoginForm, RegistrationForm, RequestResetForm,
                                 ResetPasswordForm)
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from chattie.users.utils import send_reset_email, save_picture

users = Blueprint('users', __name__)


@users.route("/login", methods=['POST', 'GET'])
def login():
    """
    Handles log in view. 
    
    If user is authenticated returns home page.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user and \
        bcrypt.check_password_hash(
            user.password,
            login_form.password.data):
            
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) \
            if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password',
                'danger')
    return render_template('login.html', 
                           title='login', 
                           login_form=login_form)


@users.route("/auto-login", methods=['POST', 'GET'])
def login_without_credentials():
    """
    View to handle login without credentials
    """
    user = User.query.filter_by(email="testchattie@testchattie.com").first()
        
    login_user(user)
    return redirect(url_for('main.home'))



@login_required
@users.route("/logout")
def logout():
    """Handles logout."""
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/register", methods=['GET', 'POST'])
def register():
    """
    Handles regiser user view.
    
    If users is autheticated, returns home page.
    
    If register form is validated, creates user and
    related profile (one to one relationship).
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password)
        db.session.add(user)
        db.session.commit()
        user_id = User.query.filter_by(
            username=form.username.data).first().id
        profile = Profile(user_id=user_id)
        db.session.add(profile)
        db.session.commit()
        flash('Your account has been created! You are now able to log in',
            'success')
        return redirect(url_for('users.login'))
    return render_template('register.html',
                           title='Register',
                           form=form)


@login_required
@users.route("/edit-profile", methods=['GET', 'POST'])
def edit_profile():
    """Handles edit profile."""
    
    user = User.query.filter_by(id=current_user.id).first()
    profile = Profile.query.filter_by(id=current_user.id).first()
    form = EditUserProfile()
    
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        profile.first_name = form.first_name.data
        profile.last_name = form.last_name.data
        profile.country = form.country.data
        profile.city = form.city.data
        profile.about = form.about.data
        picture_file = save_picture(form.image_file.data)
        profile.image_file = picture_file
        db.session.commit()
        flash(f"Your profile has been updated!", 'success')
        return redirect(url_for('main.home'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.first_name.data = profile.first_name
        form.last_name.data = profile.last_name
        form.country.data = profile.country
        form.city.data = profile.city
        form.about.data = profile.about
        form.image_file.data = profile.image_file
    image_file = url_for('static', filename='profile_pics/' + profile.image_file)
    return render_template('edit_profile.html',
                           form=form,
                           image_file=image_file,
                           title='Edit profile')


@login_required
@users.route("/change-password", methods=['GET', 'POST'])
def change_password():
    """Handles change password view."""
    user = User.query.filter_by(id=current_user.id).first()
    form = ChangePasswordForm()
    if form.validate_on_submit():
        current_user.password = bcrypt.generate_password_hash(
            form.new_password.data).decode('utf-8')
        db.session.commit()
        flash(f"Your password has been changed successfully.", 'success')
        return redirect(url_for('main.home'))
    return render_template('change_password.html',
                           form=form,
                           title='Change password')


@users.route("/reset-password", methods=['GET', 'POST'])
def reset_request():
    """Handles reset password request view."""
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash(
            'An email has been sent with instructions to reset your password.', 
            'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', 
                            title='Reset Password', 
                            form=form)
        
        
@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(
            'Your password has been updated! You are now able to log in', 
            'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', 
                           title='Reset Password', 
                           form=form)
