from chattie import bcrypt, db
from chattie.models import Profile, User
from chattie.users.forms import (ChangePasswordForm, EditUserProfile,
                                 LoginForm, RegistrationForm)
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

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
        profile.image_file = form.image_file.data
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
    return render_template('edit_profile.html',
                           form=form,
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



@login_required
@users.route("/reset-password")
def reset_password():
    """Handles reset password vie."""
    return "<h1>reset password </h1>"
