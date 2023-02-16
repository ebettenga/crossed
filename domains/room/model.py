import datetime
from marshmallow import Schema, fields
from sqlalchemy import Column, DateTime, ForeignKey, Integer
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
    created_at = Column(DateTime, default=lambda: datetime.datetime.utcnow())
    player_1_score = Column(Integer, default=0)
    player_2_score = Column(Integer, default=0)

    crossword = relationship("Crossword")

    player_1 = relationship("User", foreign_keys=[player_1_id])
    player_2 = relationship("User", foreign_keys=[player_2_id])

    def __init__(self, player_1_id, crossword_id):
        self.player_1_id = player_1_id
        self.crossword_id = crossword_id

    def __repr__(self):
        return "<id {}>".format(self.id)


class CreateRoomSchema(Schema):
    crossword_id = fields.Integer(required=True)


class RoomSchema(Schema):
    id = fields.Integer()
    player_1 = fields.Nested(UserSchema)
    player_2 = fields.Nested(UserSchema)
    crossword = fields.Nested(CrosswordSchema)
    created_at = fields.DateTime()
    player_1_score = fields.Integer()
    player_2_score = fields.Integer()
