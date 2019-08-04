import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


logger = logging.getLogger(__name__)

builtin_list = list


db = SQLAlchemy()


def init_app(app):
    # Disable track modifications, as it unnecessarily uses memory.
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    db.init_app(app)


def from_sql(row):
    """Translates a SQLAlchemy model instance into a dictionary"""
    data = row.__dict__.copy()
    data['id'] = row.id
    data.pop('_sa_instance_state')
    return data


class Participants(db.Model):
    __tablename__ = 'participants'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    surname = db.Column(db.String(255))
    email = db.Column(db.String(255))
    nickname = db.Column(db.String(255))
    created_at = db.Column(db.DateTime)

    def __repr__(self):
        return f"<Participant(name='{self.first_name} {self.surname}'"


class Events(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    start_at = db.Column(db.DateTime)
    location_id = db.Column(db.Integer)
    lifecycle_status = db.Column(db.String(255))


class Locations(db.Model):
    __tablename__ = 'locations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)


class EventProposal(db.Model):
    __tablename__ = 'event_proposals'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    created_at = db.Column(db.DateTime)
    start_at = db.Column(db.DateTime)
    status = db.Column(db.String(255))
    organiser_id = db.Column(db.Integer)


class ProposalResponse(db.Model):
    __tablename__ = 'proposal_responses'

    id = db.Column(db.Integer, primary_key=True)
    participant_id = db.Column(db.Integer)
    responded_at = db.Column(db.DateTime)
    response = db.Column(db.String(255))


class Attendance(db.Model):
    __tablename__ = 'attendance'

    id = db.Column(db.Integer, primary_key=True)
    participant_id = db.Column(db.Integer)
    event_id = db.Column(db.Integer)
    recorded_by_id = db.Column(db.Integer)


def list(limit=10, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Participants.query
             .order_by(Participants.first_name)
             .limit(limit)
             .offset(cursor))
    participants = builtin_list(map(from_sql, query.all()))
    next_page = cursor + limit if len(participants) == limit else None
    return participants, next_page


def read(id):
    result = Participants.query.get(id)
    if not result:
        return None
    return from_sql(result)


def create(data):
    book = Participants(**data)
    db.session.add(book)
    db.session.commit()
    return from_sql(book)


def update(data, id):
    book = Participants.query.get(id)
    for k, v in data.items():
        setattr(book, k, v)
    db.session.commit()
    return from_sql(book)


def delete(id):
    Participants.query.filter_by(id=id).delete()
    db.session.commit()


def _create_database():
    """
    If this script is run directly, create all the tables necessary to run the
    application.
    """
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')
    init_app(app)
    with app.app_context():
        db.create_all()
    print("All tables created")


if __name__ == '__main__':
    _create_database()
