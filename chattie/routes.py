from chattie import app, bcrypt, db
from flask import render_template, flash, redirect, url_for, request
from chattie.forms import LoginForm, RegistrationForm, CreateRoomForm
from flask_login import login_user, current_user, logout_user, login_required
from .models import User, Room


@app.route("/login", methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, login_form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='login', login_form=login_form)


@app.route("/")
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    rooms = Room.query.all()
    
    return render_template('home.html', title='home', rooms=rooms)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/edit-profile")
def edit_profile():
    return "<h1>Page for editing profile</h1>"


@app.route("/change-password")
def change_password():
    return "<h1>Change password page</h1>"


@app.route("/reset-password")
def reset_password():
    return "<h1>reset password </h1>"


@app.route("/create-room", methods=['GET', 'POST'])
@login_required
def create_room():
    form = CreateRoomForm()
    if form.validate_on_submit():
        room = Room(name=form.name.data, creator_id=current_user.id)
        db.session.add(room)
        db.session.commit()
        flash(f"Your room:{room.name} has been created!", 'success')
        return redirect(url_for('home'))    
    return render_template('create_room.html', title='Create_room', form=form)


# @app.route("/<room>")
# def room():
#     return "<h1>Home Page</h1>"


# @app.route("/update/<room>")
# def update_room():
#     return "<h1>Home Page</h1>"


# @app.route("/delete/<room>")
# def delete_room():
#     return "<h1>Home Page</h1>"