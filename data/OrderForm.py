from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class OrderForm(FlaskForm):
    surname = StringField('Surname', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    phone = StringField('Phone number', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    town = StringField('Town', validators=[DataRequired()])
    street = StringField('Street', validators=[DataRequired()])
    house = StringField('House', validators=[DataRequired()])
    flat = StringField('Flat', validators=[DataRequired()])
    promo = StringField('Promo-code', validators=[DataRequired()])
    submit = SubmitField('Pay')
