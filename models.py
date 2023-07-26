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
    city = db.Column(db.String(80), nullable=False)
    location_latitude = db.Column(db.REAL)
    location_longitude = db.Column(db.REAL)
    summary = db.Column(db.String(200))
    description = db.Column(db.String)


class Trip_visit(db.Model):
    __tablename__ = "trip_visits"

    id = db.Column(db.Integer, primary_key=True)
    visit_date = db.Column(db.Date)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    attraction_id = db.Column(db.Integer, db.ForeignKey("attractions.id"), nullable=False)




