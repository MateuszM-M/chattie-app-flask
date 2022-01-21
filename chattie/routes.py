from chattie import app
from flask import render_template

@app.route("/")
def home():
    return render_template('home.html')


@app.route("/register")
def register():
    return "<h1>Page for registration</h1>"


@app.route("/edit-profile")
def edit_profile():
    return "<h1>Page for editing profile</h1>"


@app.route("/change-password")
def change_password():
    return "<h1>Change password page</h1>"


@app.route("/reset-password")
def reset_password():
    return "<h1>reset password </h1>"


@app.route("/create-room")
def create_room():
    return "<h1>Home Page</h1>"


# @app.route("/<room>")
# def room():
#     return "<h1>Home Page</h1>"


# @app.route("/update/<room>")
# def update_room():
#     return "<h1>Home Page</h1>"


# @app.route("/delete/<room>")
# def delete_room():
#     return "<h1>Home Page</h1>"