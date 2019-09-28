import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app.app import db, login


@login.user_loader
def load_user(id):
    return shipmate.query.get(int(id))


class shipmate(db.Model, UserMixin):

    __tablename__ = "shipmates"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True, nullable=False)
    surname = db.Column(db.String(64), index=True, nullable=False)
    nickname = db.Column(db.String(64), index=True, unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    proposals = db.relationship('event', backref='organiser', lazy='dynamic')
    responses = db.relationship('proposal_response', backref='responder', lazy='dynamic')
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        return self.password_hash

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class proposal_response(db.Model):

    __tablename__ = "proposal_response"

    id = db.Column(db.Integer, primary_key=True)
    response_datetime = db.Column(db.DateTime, index=True, nullable=False, default=datetime.datetime.now)
    response = db.Column(db.String(32), index=True, nullable=False)
    response_status = db.Column(db.String(32), index=True, default="Open")
    event = db.Column(db.Integer, db.ForeignKey('events.id'))
    shipmate = db.Column(db.Integer, db.ForeignKey('shipmates.id'))


class event(db.Model):

    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(64), index=True)
    event_date = db.Column(db.Date, index=True, nullable=False)
    event_time = db.Column(db.Time, index=True, nullable=False)
    event_location = db.Column(db.String(128))
    event_status = db.Column(db.String(32),index=True, nullable=False, default="Open")
    created_at = db.Column(db.DateTime, index=True, default=datetime.datetime.now().date)
    organised_by = db.Column(db.Integer, db.ForeignKey('shipmates.id'))
    responses = db.relationship('proposal_response', backref='event_proposal', lazy='dynamic')


#    def __repr__(self):
#        return '<User {}>'.format(self.username)
