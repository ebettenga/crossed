from datetime import datetime

from marshmallow import Schema, fields
from sqlalchemy import ARRAY, DateTime, Integer, String, Boolean

from config import db

from sqlalchemy.dialects.postgresql import JSON
from flask_sqlalchemy.query import Query


class CrosswordQueryClient(Query):
    pass


class Crossword(db.Model):
    __tablename__ = "results"
    query_client = CrosswordQueryClient

    id = db.Column(Integer, primary_key=True)
    clues = db.Column(JSON, nullable=False)
    answers = db.Column(JSON, nullable=False)
    author = db.Column(String)
    circles = db.Column(ARRAY(Integer))
    date = db.Column(DateTime)
    dow = db.Column(String)
    grid = db.Column(ARRAY(String))
    gridnums = db.Column(ARRAY(Integer))
    shadecircles = db.Column(Boolean)
    col_size = db.Column(Integer)
    row_size = db.Column(Integer)

    def __init__(
        self,
        id,
        clues,
        answers,
        author,
        circles,
        date,
        dow,
        grid,
        gridnums,
        shadecircles,
        col_size,
        row_size,
    ):
        pass

    def __repr__(self):
        return "<id {}>".format(self.id)


class ResultSchema(Schema):
    id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    url = fields.Url(required=True)
    result_all = fields.Dict()
    result_no_stop_words = fields.Dict()
