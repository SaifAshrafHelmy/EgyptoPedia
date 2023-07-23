from flask import Flask
from models import db, User, City, Attraction
from cities import egypt_cities

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///egy.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db.init_app(app)


with app.app_context():
  db.create_all()

  for egypt_city in egypt_cities:
    city = City(name=egypt_city["name"])
    db.session.add(city)

  db.session.commit()



