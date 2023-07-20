from flask import Flask, request, redirect, url_for
from flask_login import (
    LoginManager,
    login_required,
    UserMixin,
    login_user,
    current_user,
    logout_user,
)
from sqlalchemy.orm import DeclarativeBase

print(DeclarativeBase)


login_manager = LoginManager()


app = Flask(__name__)
login_manager.init_app(app)


app.secret_key = "super secrety stringy"  # Change this!


users = {"foo@bar.tld": {"password": "secret"}}


class User(UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get("email")
    if email not in users:
        return
    user = User()
    user.id = email
    return user


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return """
               <form action='login' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'/>
                <input type='password' name='password' id='password' placeholder='password'/>
                <input type='submit' name='submit'/>
               </form>
               """

    email = request.form["email"]
    if email in users and request.form["password"] == users[email]["password"]:
        user = User()
        user.id = email
        login_user(user)
        return redirect(url_for("protected"))

    return "Bad login"


@app.route("/protected")
@login_required
def protected():
    return "Logged in as: " + current_user.id


@app.route("/logout")
def logout():
    logout_user()
    return "Logged out"


@login_manager.unauthorized_handler
def unauthorized_handler():
    return "Unauthorized", 401
