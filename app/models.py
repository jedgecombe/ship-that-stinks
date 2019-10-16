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
    nickname = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    password_hash = db.Column(db.String(128), nullable=False)
    # TODO sort out these relationships
    events = db.relationship('Event', back_populates='user', lazy='dynamic')
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
    is_active = db.Column(db.Boolean, default=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)

    user = db.relationship('User', back_populates='responses')
    event = db.relationship('Event', back_populates='responses')


class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(64), nullable=False)
    start_at = db.Column(db.DateTime, nullable=False)
    end_at = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(128))
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    notice_days = db.Column(db.Float, nullable=False)
    organised_by = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)

    user = db.relationship('User', back_populates='events')
    responses = db.relationship('ProposalResponse', back_populates='event', lazy='dynamic')
    attendees = db.relationship('Attendance', back_populates='event', lazy='dynamic')


class Attendance(db.Model):
    __tablename__ = "attendance"

    id = db.Column(db.Integer, primary_key=True, index=True)
    recorded_at = db.Column(db.DateTime, default=datetime.now())
    is_active = db.Column(db.Boolean, nullable=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)

    user = db.relationship('User', back_populates='attendances')
    event = db.relationship('Event', back_populates='attendees')
