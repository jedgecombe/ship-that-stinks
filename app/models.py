from datetime import datetime

from citext import CIText
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import and_
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
    nickname = db.Column(db.String(64), unique=True, nullable=False)
    # for some reason adding unique constraint makes alembic hang
    email = db.Column(CIText(),  nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    # indicator for user with special privileges e.g. arranging end of cycle event
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    # TODO add is_viewer (or something) - can't create events and isn't included in the scoring. Should we have a roles table?
    password_hash = db.Column(db.String(128), nullable=False)
    # TODO sort out these relationships
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
    event_id = db.Column(db.Integer, db.ForeignKey('event_ids.id'), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)

    user = db.relationship('User', back_populates='responses')
    event = db.relationship('Event', back_populates='responses')


class EventEvents(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True, index=True)
    # when update was created
    # TODO add nullable = False
    update_created_at = db.Column(db.DateTime, nullable=True, default=datetime.now())
    # is this most recent update
    # TODO add nullable = False
    is_active_update = db.Column(db.Boolean, nullable=True, default=True)

    # event details
    # TODO add nullable = False
    event_id = db.Column(db.Integer, nullable=True)
    # event_id = db.Column(db.Integer, db.ForeignKey('event_ids.id'), index=True)
    name = db.Column(db.String(64), nullable=False)
    start_at = db.Column(db.DateTime, nullable=False)
    end_at = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(128))
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    # has the organiser confirmed the event is going ahead
    is_confirmed = db.Column(db.Boolean, nullable=False, default=True)
    # number of days created in advance of start
    notice_days = db.Column(db.Integer, nullable=False)
    # multiplier used for the notice score component
    notice_mult = db.Column(db.Float, nullable=False)

    # TODO add nullable = False
    has_happened = db.Column(db.Boolean, default=False)
    # when the event was created
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    # TODO delete organised_by
    organised_by = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)

    # number of attendees recorded - NULL, until attendance is recorded
    attendee_cnt = db.Column(db.Integer)
    # multiplier user for the attendee score component
    attendee_mult = db.Column(db.Float)
    # points per attendee
    points_pp = db.Column(db.Float)

    event = db.relationship('Event', back_populates='updates')


class Event(db.Model):
    __tablename__ = "event_ids"
    id = db.Column(db.Integer, primary_key=True, index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    organised_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False,
                             index=True)
    # current_info = db.relationship('EventEvents', primaryjoin=and_(
    #     id == EventEvents.event_id, EventEvents.is_active_update == True,
    #     EventEvents.is_active == True))
    updates = db.relationship('EventEvents', back_populates='event', lazy='dynamic')
    organiser = db.relationship('User', back_populates='events_organised')
    attendees = db.relationship('Attendance', back_populates='event', lazy='dynamic')
    responses = db.relationship('ProposalResponse', back_populates='event',
                                lazy='dynamic')


class Attendance(db.Model):
    __tablename__ = "attendance"

    id = db.Column(db.Integer, primary_key=True, index=True)
    recorded_at = db.Column(db.DateTime, default=datetime.now())
    is_active = db.Column(db.Boolean, nullable=True)
    event_id = db.Column(db.Integer, nullable=True)
    # event_id = db.Column(db.Integer, db.ForeignKey('event_ids.id'), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)

    user = db.relationship('User', back_populates='attendances')
    event = db.relationship('Event', back_populates='attendees')
