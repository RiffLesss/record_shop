from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email


class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    email = StringField("Email: ", validators=[Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Repeat the password', validators=[DataRequired()])
    submit = SubmitField('Log in')
