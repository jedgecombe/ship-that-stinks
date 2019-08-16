import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from ship_that_stinks.database.table_definitions import Shipmates

logger = logging.getLogger(__name__)

db = SQLAlchemy()
# class Shipmates(db.Model):
#     __tablename__ = "shipmates"
#
#     id = db.Column(db.Integer, primary_key=True)
#     first_name = db.Column(db.String(255))
#     surname = db.Column(db.String(255))
#     email = db.Column(db.String(255))
#     nickname = db.Column(db.String(255))
#     created_at = db.Column(db.DateTime)
#     is_authenticated = db.Column(db.Boolean)
#     is_anonymous = db.Column(db.Boolean)
#     is_active = db.Column(db.Boolean)
#     password_hash = db.Column(db.String(255))
#
#     def __repr__(self):
#         return f"<Shipmate(name='{self.first_name} {self.surname}'"



class DbUtils:
    @classmethod
    def insert(cls, table, data):
        add_statement = Shipmates(**data)
        db.session.add(add_statement)
        db.session.commit()
        return cls.from_sql(add_statement)

    @classmethod
    def read(cls, table, id):
        result = Shipmates.query.get(id)
        if not result:
            return None
        return cls.from_sql(result)

    @classmethod
    def list(cls, table, limit=10, cursor=None):
        cursor = int(cursor) if cursor else 0
        query = Shipmates.query.order_by(Shipmates.id).limit(limit).offset(cursor)
        results = list(map(cls.from_sql, query.all()))
        next_page = cursor + limit if len(results) == limit else None
        return results, next_page

    @classmethod
    def update(cls, table, data, id):
        shipmate = Shipmates.query.get(id)
        for k, v in data.items():
            b = 1
        #     # row.k = v
            setattr(shipmate, k, v)
            a = 1
        db.session.commit()
        # db.session.flush()
        return cls.from_sql(shipmate)

    @classmethod
    def delete(cls, table, id):
        Shipmates.query.filter_by(id=id).delete()
        db.session.commit()

    @classmethod
    def from_sql(cls, row):
        """Translates a SQLAlchemy model instance into a dictionary"""
        data = row.__dict__.copy()
        data["id"] = row.id
        data.pop("_sa_instance_state")
        return data





