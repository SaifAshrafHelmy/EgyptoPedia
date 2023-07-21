from flask import Flask, request, redirect, url_for
from flask_login import (
    LoginManager,
    login_required,
    UserMixin,
    login_user,
    current_user,
    logout_user,
)
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# @Todo List
# """
# implement WTforms
#  """
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True)
    username = Column("username", String(20), nullable=False, unique=True)
    password = Column("password", String(20), nullable=False)
    name = Column("name", String, nullable=False)

    def __init__(self, id, username, password, name):
        self.id = id
        self.username = username
        self.password = password
        self.name = name

    def __repr__(self):
        return f"({self.id}) {self.username} {self.name}"


engine = create_engine("sqlite:///egyptopedia.db", echo=True)
Base.metadata.create_all(bind=engine)


Session = sessionmaker(bind=engine)
session = Session()


# user1 = User(3, "ahmed", "123", "Ahmed Sabry")
# session.add(user1)
# session.commit()

results = session.query(User).filter(User.id == 5)
for r in results:
    print(r)


##flask-login stuff
login_manager = LoginManager()


app = Flask(__name__)
login_manager.init_app(app)


app.secret_key = "super secrety stringy"  # Change this!


users = {"foo@bar.tld": {"password": "secret"}}


class FLUser(UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = FLUser()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get("email")
    if email not in users:
        return
    user = FLUser()
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
        user = FLUser()
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
