from sqlalchemy import Column, Integer, String
from database import Base
from flask_login import UserMixin


class User(Base, UserMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True, nullable=False)
    password = Column(String(80), nullable=False)

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password

    def __repr__(self):
        return f"<User {self.username!r}>"
    
    def get(user_id):
        from database import db_session
        return db_session.query(User).get(user_id)
    

