import datetime

from flask_wtf import FlaskForm
from wtforms import (BooleanField, PasswordField, RadioField, StringField,
                     SubmitField)
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
from wtforms_components import DateRange, TimeField


class EventForm(FlaskForm):
    event_name = StringField('Event name', validators=[DataRequired()])
    event_date = DateField('Event date', validators=[DataRequired(), DateRange(min=datetime.datetime.today().date())])
    event_time = TimeField('Event time', validators=[DataRequired()])
    event_location = StringField('Event location', validators=[DataRequired()])
    submit = SubmitField('Propose Event')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class ResponseForm(FlaskForm):
    response = RadioField(choices=[('Accepted', 'Accept'), ('Declined', 'Decline')])
    submit = SubmitField('Send Response')


class AccountForm(FlaskForm):
    password = PasswordField('Change password', validators=[DataRequired()])
    submit = SubmitField('Update')
