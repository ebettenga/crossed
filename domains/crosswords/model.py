from marshmallow import Schema, ValidationError, fields
from sqlalchemy import ARRAY, Date, Integer, String, Boolean

from config import db

from sqlalchemy.dialects.postgresql import JSON


class Crossword(db.Model):
    __tablename__ = "crosswords"

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
    title = db.Column(String)

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
        title,
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
        self.title = title

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


class CrosswordSchema(Schema):
    id = fields.Int(dump_only=True)
    clues = fields.Dict()
    answers = fields.Dict()
    author = fields.String()
    circles = fields.List(fields.Integer())
    date = fields.Date()
    dow = fields.String()
    grid = fields.List(fields.String())
    gridnums = fields.List(fields.Integer())
    shadecircles = fields.Boolean()
    col_size = fields.Integer()
    row_size = fields.Integer()
    jnote = fields.String()
    notepad = fields.String()


def is_dow(dow_string):
    if dow_string not in [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]:
        raise ValidationError("dow must be a capitilized weekday")


class CrosswordQuerySchema(Schema):
    page = fields.Integer()
    limit = fields.Integer()
    dow = fields.String(validate=is_dow)
    col_size = fields.Integer()
    row_size = fields.Integer()
