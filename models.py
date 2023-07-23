from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# create the extension
db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def get(user_id):
        return db.session.query(User).get(user_id)


class Attraction(db.Model):
    __tablename__ = "attractions"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey("cities.id"), nullable=False)
    location_longitude = db.Column(db.REAL)
    location_latitude = db.Column(db.REAL)
    summary = db.Column(db.String(200))
    description = db.Column(db.String)

    city = db.relationship("City", back_populates="attractions")


class City(db.Model):
    __tablename__ = "cities"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    attractions = db.relationship("Attraction", back_populates="city")
