from datetime import datetime

from marshmallow import Schema, fields
from sqlalchemy import DateTime

from config import db

from sqlalchemy.dialects.postgresql import JSON
from flask_sqlalchemy.query import Query


class ResultQueryClient(Query):
    def filter_by_result(self, result: str):
        if result:
            self = self.filter((Result.tag_group_type == result))
        return self


class Result(db.Model):
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String())
    result_all = db.Column(JSON)
    result_no_stop_words = db.Column(JSON)
    created_at = db.Column(DateTime, nullable=False, default=lambda: datetime.utcnow())

    def __init__(self, url, result_all, result_no_stop_words):
        self.url = url
        self.result_all = result_all
        self.result_no_stop_words = result_no_stop_words

    def __repr__(self):
        return '<id {}>'.format(self.id)


class ResultSchema(Schema):
    id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    url = fields.Url(required=True)
    result_all = fields.Dict()
    result_no_stop_words = fields.Dict()
