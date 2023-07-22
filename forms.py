from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length


class MyForm(FlaskForm):
    username = StringField('username', validators=[DataRequired( message="You must enter the username." ), Length(min=3, max=20, message="Username must be 3-20 characters")])
    password = PasswordField('password', validators=[DataRequired( message="You must enter the password."), Length(min=3, max=20, message="Password must be 3-20 characters")])

