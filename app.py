from flask import Flask, render_template, redirect, request, flash
from database import db_session, init_db
from models import User
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
login_manager = LoginManager()
from sqlalchemy import create_engine, MetaData, Table
from flask_bcrypt import Bcrypt


# from markupsafe import escape



app = Flask(__name__)

bcrypt = Bcrypt(app)



@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


engine = create_engine('sqlite:///database.db')
metadata = MetaData(bind=engine)
users = Table('users', metadata, autoload=True)



login_manager.init_app(app)
app.secret_key = b'_5#@@y2L"F5Q8d\n\xec]/'


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)




@app.route("/")
def hello_world():
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated == True:
        flash('You are already logged in.', 'warning')
        return redirect("/")
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = users.select(users.c.username == username).execute().first()
        if(user):
            if (bcrypt.check_password_hash(user.password, password)):
              M_User = load_user(user.id)
              login_user(M_User, remember=True);
              flash('Logged in successfully.', 'success')
              return redirect("/")
            
        flash('Invalid credentials, try again.', 'error')
        return render_template("login.html")



    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        raw_password = request.form.get("password")
        pw_hash = bcrypt.generate_password_hash(raw_password)

        u = User(username, pw_hash)
        db_session.add(u)
        db_session.commit()

        return render_template("register.html")

    return render_template("register.html")



@app.route("/protected")
@login_required
def myProtected():
    return "YOU HAVE ACCESS"

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")








if __name__ == '__main__':
    # Initialize the database
    init_db()

    # Run the Flask application
    app.run()
