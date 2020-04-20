from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    email = StringField("Email: ", validators=[Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Log in')