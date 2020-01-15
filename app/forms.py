import datetime

from flask_wtf import FlaskForm
from wtforms import (BooleanField, PasswordField, RadioField, StringField,
                     SubmitField, SelectMultipleField, widgets)
from wtforms.fields.html5 import DateField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from wtforms_components import DateRange, TimeField

from app.models import User


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class EventForm(FlaskForm):
    name = StringField('Event name', validators=[DataRequired()])
    start_date = DateField('Event date', validators=[DataRequired(), DateRange(
        min=datetime.datetime.today().date())])
    start_time = TimeField('Event time', validators=[DataRequired()])
    end_date = DateField('Event end date', validators=[DataRequired(), DateRange(
        min=datetime.datetime.today().date())])
    end_time = TimeField('Event end time', validators=[DataRequired()])
    location = StringField('Event location', validators=[DataRequired()])
    submit = SubmitField('Propose Event')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class ResponseForm(FlaskForm):
    response = RadioField(choices=[('Accepted', 'Accept'), ('Declined', 'Decline')])
    submit = SubmitField('Send Response')


class AccountForm(FlaskForm):
    password = PasswordField('Change password', validators=[DataRequired()])
    submit = SubmitField('Update')


class RegisterAttendanceForm(FlaskForm):
    users = User.query.all()
    user_details = [(user.id, user.username) for user in users]
    user_ids = MultiCheckboxField('Label', choices=user_details)

    submit = SubmitField('Register attendance')

