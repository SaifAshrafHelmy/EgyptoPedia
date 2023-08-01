import datetime
import html
import os
from flask import Flask, render_template, redirect, request, flash
from models import db, User, Attraction, Trip_visit
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
login_manager = LoginManager()
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from forms import MyForm
from sqlalchemy import func




app = Flask(__name__)

bcrypt = Bcrypt(app)
# csrf = CSRFProtect(app)



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


uniqueCities = [];
def getUniqueCitiesFromDB():
    # cities = db.session.query(Attraction.city).distinct().order_by(Attraction.city.asc()).all()
    # for city in cities:
    #     uniqueCities.append(city[0])
    global uniqueCities
    subquery = db.session.query(Attraction.city, func.count(Attraction.id).label('attraction_count')) \
            .group_by(Attraction.city) \
            .subquery()

    cities_with_attractions_count = db.session.query(subquery.c.city, subquery.c.attraction_count) \
                            .order_by(subquery.c.attraction_count.desc()) \
                            .all()

    # Extract the city names and the attraction counts as a list of dictionaries
    uniqueCities = [ {'city': city, 'attraction_count': attraction_count} for city, attraction_count in cities_with_attractions_count]






with app.app_context():
    getAttractionsFromDB()
    getUniqueCitiesFromDB()



@app.route("/attractions", methods=["GET", "POST"])
@login_required
def viewAttractions():
    if request.method == "GET":
        return render_template("attractions.html", attractions = myAttractions, uniqueCities=uniqueCities)
    else:
        attraction_name = request.form.get("attraction_name")
        escaped_attraction_name = html.escape(attraction_name)
        search_term = "%{}%".format(escaped_attraction_name)
        results = db.session.query(Attraction).filter(Attraction.name.like(search_term)).all()

        searchedAttractions = [];

        for attraction in results:
            attraction = attraction.__dict__

            slug = attraction["name"].replace(' ', '&')
            attraction["slug"] = slug
            searchedAttractions.append(attraction)


        return render_template("attractions.html", attractions = searchedAttractions, searchTerm = escaped_attraction_name, uniqueCities=uniqueCities )



@app.route("/attractions/bycity/<city>", methods=["GET"])
@login_required
def viewAttractionsInCity(city):
    escaped_attraction_city = html.escape(city)
    filter_city = "%{}%".format(escaped_attraction_city)
    results = db.session.query(Attraction).filter(Attraction.city.like(filter_city)).all()

    searchedAttractions = [];

    for attraction in results:
        attraction = attraction.__dict__

        slug = attraction["name"].replace(' ', '&')
        attraction["slug"] = slug
        searchedAttractions.append(attraction)


    return render_template("attractions.html", attractions = searchedAttractions, filterCity = escaped_attraction_city, uniqueCities=uniqueCities)


# @app.route("/attractions/city", methods=["GET", "POST"])
# @login_required
# def viewAttractionsInCity():
#     attraction_city = request.args.get("attraction_city")
#     escaped_attraction_city = html.escape(attraction_city)
#     filter_city = "%{}%".format(escaped_attraction_city)
#     results = db.session.query(Attraction).filter(Attraction.city.like(filter_city)).all()

#     searchedAttractions = [];

#     for attraction in results:
#         attraction = attraction.__dict__

#         slug = attraction["name"].replace(' ', '&')
#         attraction["slug"] = slug
#         searchedAttractions.append(attraction)


#     return render_template("attractions.html", attractions = searchedAttractions, filterCity = escaped_attraction_city, uniqueCities=uniqueCities)



@app.route("/mytrip")
@login_required
def tl():
    data = db.session.query(Trip_visit, Attraction).join(Attraction).filter(Trip_visit.user_id == current_user.id).order_by(Trip_visit.visit_date.asc()).all()

    return render_template("trip_final.html", data = data)


@app.route("/addtotrip", methods=["POST"])
@login_required
def addToTrip():
    attraction_id = request.form.get("attraction_id")
    date = request.form.get("date")
    datetime_obj = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    print(attraction_id)
    print(datetime_obj)

    trip_visit = Trip_visit(visit_date=datetime_obj, attraction_id=attraction_id, user_id =current_user.id )
    db.session.add(trip_visit)
    db.session.commit()


    print("RECEIVED")
    return  '', 204


@app.route("/removefromtrip", methods=["POST"])
@login_required
def removeFromTrip():
    trip_visit_id = request.form.get("trip_visit_id")
    db.session.query(Trip_visit).filter(Trip_visit.id == trip_visit_id ).delete()
    db.session.commit()

    return redirect('/mytrip')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")







if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
    app.run(debug=True)




