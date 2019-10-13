import datetime

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

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True, nullable=False)
    surname = db.Column(db.String(64), index=True, nullable=False)
    nickname = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(128), index=True, unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    proposals = db.relationship('Event', backref='organiser', lazy='dynamic')
    responses = db.relationship('ProposalResponse', backref='responder', lazy='dynamic')
    attendances = db.relationship('Attendance', back_populates='user')
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        return self.password_hash

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class ProposalResponse(db.Model):
    __tablename__ = "proposal_responses"

    id = db.Column(db.Integer, primary_key=True)
    # TODO change col name to 'timestamp'
    response_datetime = db.Column(db.DateTime, index=True, nullable=False,
                                  default=datetime.datetime.now)
    # TODO change col name to 'description'
    # TODO should we have a responses table with 'description' and 'id' as columns?
    response = db.Column(db.String(32), index=True, nullable=False)
    # TODO change col name to 'status'
    response_status = db.Column(db.String(32), index=True, default="Open")
    event = db.Column(db.Integer, db.ForeignKey('events.id'))
    user = db.Column(db.Integer, db.ForeignKey('users.id'))


class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    start_date = db.Column(db.Date, index=True, nullable=False)
    start_time = db.Column(db.Time, index=True, nullable=False)
    end_date = db.Column(db.Date, index=True, nullable=False)
    end_time = db.Column(db.Time, index=True, nullable=False)
    location = db.Column(db.String(128))
    status = db.Column(db.String(32),index=True, nullable=False, default="Open")
    created_at = db.Column(db.DateTime, index=True, default=datetime.datetime.now())
    organised_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    responses = db.relationship('ProposalResponse', backref='event_proposal', lazy='dynamic')
    attendees = db.relationship('Attendance', back_populates='event')


class Attendance(db.Model):
    __tablename__ = "attendance"

    id = db.Column(db.Integer, primary_key=True)
    recorded_at = db.Column(db.DateTime, index=True, default=datetime.datetime.now())
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # TODO add is_current to log people messing with stuff

    user = db.relationship('User', back_populates='attendances')
    event = db.relationship('Event', back_populates='attendees')



# attendance_association_table = db.Table('association',
#                                      Base.metadata,
#                                      db.Column('shipmate_id', db.Integer, db.ForeignKey('shipmate_id')),
#                                      db.Column('event_id', db.Integer, db.ForeignKey ('event_id')))