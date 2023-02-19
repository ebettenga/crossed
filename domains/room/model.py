import datetime
from marshmallow import Schema, fields
from marshmallow.validate import OneOf
from sqlalchemy import ARRAY, Column, DateTime, ForeignKey, Identity, Integer, String
from sqlalchemy.orm import relationship
from config import db

from domains.crosswords.model import CrosswordSchema

from domains.user.model import UserSchema


class Room(db.Model):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True)
    player_1_id = Column(
        Integer, ForeignKey("users.id", name="room_user_1_id_fkey"), nullable=False
    )
    player_2_id = Column(Integer, ForeignKey("users.id", name="room_user_2_id_fkey"))
    crossword_id = Column(
        Integer,
        ForeignKey("crosswords.id", name="room_crossword_id_fkey"),
        nullable=False,
    )
    found_letters = Column(ARRAY(String))
    player_1_score = Column(Integer, default=0)
    player_2_score = Column(Integer, default=0)
    created_at = Column(DateTime, default=lambda: datetime.datetime.utcnow())
    difficulty = Column(String)

    crossword = relationship("Crossword")
    player_1 = relationship("User", foreign_keys=[player_1_id])
    player_2 = relationship("User", foreign_keys=[player_2_id])

    def __init__(self, player_1_id, crossword_id, difficulty):
        self.player_1_id = player_1_id
        self.crossword_id = crossword_id
        self.difficulty = difficulty

    def __repr__(self):
        return "<id {}>".format(self.id)


class JoinRoomSchema(Schema):
    user_id = fields.Integer(required=True)
    difficulty = fields.String(validate=OneOf(["easy", "medium", "hard"]))


class SubmitSquareSchema(Schema):
    x = fields.Integer()
    y = fields.Integer()
    guess = fields.String()


class RoomSchema(Schema):
    id = fields.Integer()
    found_letters = fields.List(fields.String())
    player_1 = fields.Nested(UserSchema)
    player_2 = fields.Nested(UserSchema)
    crossword = fields.Nested(
        CrosswordSchema(
            exclude=[
                "answers",
                "grid",
            ]
        )
    )
    created_at = fields.DateTime()
    player_1_score = fields.Integer()
    player_2_score = fields.Integer()
    difficulty = fields.String()
