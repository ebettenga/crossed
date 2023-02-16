from datetime import datetime

from marshmallow import Schema, fields
from sqlalchemy import ARRAY, Date, Integer, String, Boolean

from config import db

from sqlalchemy.dialects.postgresql import JSON
from flask_sqlalchemy.query import Query


class CrosswordQueryClient(Query):
    pass


class Crossword(db.Model):
    __tablename__ = "crosswords"
    query_client = CrosswordQueryClient

    id = db.Column(Integer, primary_key=True)
    clues = db.Column(JSON, nullable=False)
    answers = db.Column(JSON, nullable=False)
    author = db.Column(String)
    circles = db.Column(ARRAY(Integer))
    date = db.Column(Date)
    dow = db.Column(String)
    grid = db.Column(ARRAY(String))
    gridnums = db.Column(ARRAY(Integer))
    shadecircles = db.Column(Boolean)
    col_size = db.Column(Integer)
    row_size = db.Column(Integer)
    jnote = db.Column(String)
    notepad = db.Column(String)

    def __init__(
        self,
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
        jnotes,
        notepad,
        *args,
        **kwargs,
    ):
        self.clues = clues
        self.answers = answers
        self.author = author
        self.circles = circles
        self.date = date
        self.dow = dow
        self.grid = grid
        self.gridnums = gridnums
        self.shadecircles = shadecircles
        self.col_size = col_size
        self.row_size = row_size
        self.jnote = jnotes
        self.notepad = notepad

        if kwargs:
            for key, item in kwargs.items():
                if item and key not in [
                    "size",
                    "title",
                    "editor",
                    "copyright",
                    "publisher",
                    "hastitle",
                ]:
                    print(f"{key} {item}")

    def __repr__(self):
        return "<id {}>".format(self.id)


class ResultSchema(Schema):
    id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    url = fields.Url(required=True)
    result_all = fields.Dict()
    result_no_stop_words = fields.Dict()
