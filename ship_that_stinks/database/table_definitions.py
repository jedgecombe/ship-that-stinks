"""Contains all table definitions"""

import logging

from flask_sqlalchemy import SQLAlchemy


logger = logging.getLogger(__name__)


db = SQLAlchemy()


class Shipmates(db.Model):
    __tablename__ = "shipmates"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    surname = db.Column(db.String(255))
    email = db.Column(db.String(255))
    nickname = db.Column(db.String(255))
    created_at = db.Column(db.DateTime)
    is_authenticated = db.Column(db.Boolean)
    is_anonymous = db.Column(db.Boolean)
    is_active = db.Column(db.Boolean)
    password_hash = db.Column(db.String(255))

    def __repr__(self):
        return f"<Shipmate(name='{self.first_name} {self.surname}'"


class Events(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    start_at = db.Column(db.DateTime)
    location_id = db.Column(db.Integer)
    lifecycle_status = db.Column(db.String(255))


class Locations(db.Model):
    __tablename__ = "locations"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)


class EventProposal(db.Model):
    __tablename__ = "event_proposals"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime)
    status = db.Column(db.String(255))
    organiser_id = db.Column(db.Integer)


class ProposalResponse(db.Model):
    __tablename__ = "proposal_responses"

    id = db.Column(db.Integer, primary_key=True)
    shipmate_id = db.Column(db.Integer)
    responded_at = db.Column(db.DateTime)
    response = db.Column(db.String(255))
    event_proposal_id = db.Column(db.Integer)


class Attendance(db.Model):
    __tablename__ = "attendance"

    id = db.Column(db.Integer, primary_key=True)
    shipmate_id = db.Column(db.Integer)
    event_id = db.Column(db.Integer)
    recorded_by_id = db.Column(db.Integer)
