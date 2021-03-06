from datetime import datetime


from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from app import db, login


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, index=True)
    first_name = db.Column(db.String(64), nullable=False)
    surname = db.Column(db.String(64), nullable=False)
    username = db.Column(db.String(64), unique=True, nullable=False)
    # for some reason adding unique constraint makes alembic hang
    email = db.Column(db.Text,  nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    # TODO add is_viewer (or something) - can't create events and isn't included in the scoring. Should we have a roles table?
    password_hash = db.Column(db.String(128), nullable=False)
    events_organised = db.relationship('Event', back_populates='organiser', lazy='dynamic')
    responses = db.relationship('ProposalResponse', back_populates='user', lazy='dynamic')
    attendances = db.relationship('Attendance', back_populates='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        return self.password_hash

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class ProposalResponse(db.Model):
    __tablename__ = "proposal_responses"

    id = db.Column(db.Integer, primary_key=True, index=True)
    created_at = db.Column(db.DateTime,  nullable=False,  default=datetime.now())
    description = db.Column(db.String(32), nullable=False, default="Accept")
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)

    user = db.relationship('User', back_populates='responses')
    event = db.relationship('Event', back_populates='responses')


class EventEvents(db.Model):
    __tablename__ = "event_events"

    id = db.Column(db.Integer, primary_key=True, index=True)
    # when update was created
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    # is this most recent update
    is_active_update = db.Column(db.Boolean, nullable=False, default=True)

    # event details
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), index=True,
                         nullable=False)
    name = db.Column(db.String(64), nullable=False)
    start_at = db.Column(db.DateTime, nullable=False)
    # TODO change from end_at to duration, from which end_at can be inferred
    end_at = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(128))
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    event = db.relationship('Event', back_populates='updates')


class Event(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    organised_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False,
                             index=True)
    cycle_id = db.Column(db.Integer, db.ForeignKey('cycles.id'), index=True,
                         nullable=False)
    has_happened = db.Column(db.Boolean, default=False, nullable=True)
    # number of days created in advance of start
    notice_days = db.Column(db.Integer, nullable=False)
    # multiplier used for the notice score component
    notice_mult = db.Column(db.Float, nullable=False)
    # number of attendees recorded - NULL, until attendance is recorded
    attendee_cnt = db.Column(db.Integer, nullable=True)
    # multiplier user for the attendee score component
    attendee_mult = db.Column(db.Float, nullable=True)
    # points per attendee
    points_pp = db.Column(db.Float, nullable=True)
    # has the organiser confirmed the event is going ahead
    # TODO add is_confirmed
    # is_confirmed = db.Column(db.Boolean, nullable=True, default=True)

    updates = db.relationship('EventEvents', back_populates='event', lazy='dynamic')
    organiser = db.relationship('User', back_populates='events_organised')
    attendees = db.relationship('Attendance', back_populates='event', lazy='dynamic')
    responses = db.relationship('ProposalResponse', back_populates='event',
                                lazy='dynamic')
    cycle = db.relationship('Cycle', back_populates='events')


class Attendance(db.Model):
    __tablename__ = "attendance"

    id = db.Column(db.Integer, primary_key=True, index=True)
    recorded_at = db.Column(db.DateTime, default=datetime.now())
    is_active = db.Column(db.Boolean, nullable=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)

    user = db.relationship('User', back_populates='attendances')
    event = db.relationship('Event', back_populates='attendees')


class Cycle(db.Model):
    __tablename__ = "cycles"

    id = db.Column(db.Integer, primary_key=True, index=True)
    start_at = db.Column(db.Date, nullable=False)
    end_at = db.Column(db.Date, nullable=False)

    events = db.relationship('Event', back_populates='cycle', lazy='dynamic')
