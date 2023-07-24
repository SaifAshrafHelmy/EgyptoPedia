from flask import Flask, render_template, redirect, request, flash
from models import db, User, Attraction
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
login_manager = LoginManager()
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from forms import MyForm




app = Flask(__name__)

bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)



# initialize the login manager
login_manager.init_app(app)
app.secret_key = b'_5#@@y2L"F5Q8d\n\xec]/'


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///egy.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# initialize the app with the database extension
db.init_app(app)

# create all db tables
with app.app_context():
    db.create_all()




@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)




@app.route("/")
def hello_world():
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    

    if current_user.is_authenticated:
        flash('You are already logged in.', 'warning')
        return redirect("/")
    
    form = MyForm()

    if request.method == "POST":
        if form.validate_on_submit():
            username = request.form.get("username")
            password = request.form.get("password")

            try:
                user = db.session.execute(db.select(User).filter_by(username=username)).scalar_one()
            except:
                user = None

            if(user):
                if (bcrypt.check_password_hash(user.password, password)):
                    M_User = load_user(user.id)
                    login_user(M_User, remember=True);
                    flash('Logged in successfully.', 'success')
                    return redirect("/")
                else:
                    flash("Wrong password, try again.", 'error')
                    
            else:
                flash("Username doesn't exit", 'error')


    return render_template("login.html", form=form)


        



@app.route("/register", methods=["GET", "POST"])
def register():
    
    if current_user.is_authenticated:
        flash('You are already logged in.', 'warning')
        return redirect("/")

    form = MyForm()

    if request.method == "POST":
        if form.validate_on_submit():

            username = request.form.get("username")
            raw_password = request.form.get("password")
            pw_hash = bcrypt.generate_password_hash(raw_password)

            user = User(username = username,password =  pw_hash)
            db.session.add(user)
            db.session.commit()

            M_User = load_user(user.id)
            login_user(M_User, remember=True);
            flash('Registered successfully.', 'success')
            return redirect("/")


    return render_template("register.html", form=form)

myAttractions = [];

def getAttractionsFromDB():
    attractions = db.session.execute(db.select(Attraction)).scalars()
    
    for attraction in attractions:

        attraction = attraction.__dict__

        slug = attraction["name"].replace(' ', '&')
        attraction["slug"] = slug

        myAttractions.append(attraction)


with app.app_context():
    getAttractionsFromDB()


@app.route("/attractions")
@login_required
def viewAttractions():
    

    return render_template("attractions.html", attractions = myAttractions)


@app.route("/protected")
@login_required
def myProtected():
    return "YOU HAVE ACCESS"


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")








if __name__ == "__main__":
    app.run(debug=True)




    

