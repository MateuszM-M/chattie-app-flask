from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Home Page. There will be login or room management page</h1>"


@app.route("/register")
def home():
    return "<h1>Page for registration</h1>"


@app.route("/edit-profile")
def home():
    return "<h1>Page for editing profile</h1>"


@app.route("/change-password")
def home():
    return "<h1>Change password page</h1>"


@app.route("/reset-password")
def home():
    return "<h1>reset password </h1>"


@app.route("/create-room")
def home():
    return "<h1>Home Page</h1>"


@app.route("/<room>")
def home():
    return "<h1>Home Page</h1>"


@app.route("/update/<room>")
def home():
    return "<h1>Home Page</h1>"


@app.route("/delete/<room>")
def home():
    return "<h1>Home Page</h1>"
