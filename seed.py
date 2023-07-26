from flask import Flask
from models import db, User, Attraction, Trip_visit
from cities import egypt_cities
from attractionsList import attractions 
import datetime

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///egy.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db.init_app(app)


with app.app_context():
  db.create_all()

  for attraction in attractions:
    db.session.add(Attraction(**attraction))

  db.session.commit()


with app.app_context():
  v1 = Trip_visit(visit_date = datetime.datetime(2024,9,15), user_id = 1, attraction_id = 9 )    
  db.session.add(v1)
  db.session.commit()  
