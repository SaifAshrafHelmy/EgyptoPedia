from flask import Flask
from models import db, User, Attraction
from cities import egypt_cities
from attractionsList import attractions 

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///egy.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db.init_app(app)


with app.app_context():
  db.create_all()

  for attraction in attractions:
    db.session.add(Attraction(**attraction))

  db.session.commit()



