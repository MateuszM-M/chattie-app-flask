from chattie import bcrypt, db
from chattie.models import Profile, User
from chattie.users.forms import LoginForm, RegistrationForm
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
@users.route("/edit-profile")
def edit_profile():
    """Handles edit profile."""
    return "<h1>Page for editing profile</h1>"


@login_required
@users.route("/change-password")
def change_password():
    """Handles change password view."""
    return "<h1>Change password page</h1>"


@login_required
@users.route("/reset-password")
def reset_password():
    """Handles reset password vie."""
    return "<h1>reset password </h1>"
