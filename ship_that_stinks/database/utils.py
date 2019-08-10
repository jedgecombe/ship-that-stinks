import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


logger = logging.getLogger(__name__)

db = SQLAlchemy()


class DbUtils:
    @classmethod
    def insert(cls, table, data):
        add_statement = table(**data)
        db.session.add(add_statement)
        db.session.commit()
        return cls.from_sql(add_statement)

    @classmethod
    def read(cls, table, id):
        result = table.query.get(id)
        if not result:
            return None
        return cls.from_sql(result)

    @classmethod
    def list(cls, table, limit=10, cursor=None):
        cursor = int(cursor) if cursor else 0
        query = table.query.order_by(table.id).limit(limit).offset(cursor)
        results = list(map(cls.from_sql, query.all()))
        next_page = cursor + limit if len(results) == limit else None
        return results, next_page

    @classmethod
    def update(cls, table, data, id):
        row = table.query.get(id)
        for k, v in data.items():
            setattr(row, k, v)
        db.session.commit()
        return cls.from_sql(row)

    @classmethod
    def delete(cls, table, id):
        table.query.filter_by(id=id).delete()
        db.session.commit()

    @classmethod
    def from_sql(cls, row):
        """Translates a SQLAlchemy model instance into a dictionary"""
        data = row.__dict__.copy()
        data["id"] = row.id
        data.pop("_sa_instance_state")
        return data





