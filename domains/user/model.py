

from datetime import datetime

from marshmallow import Schema, fields
from sqlalchemy import DateTime
from config import db
from flask_sqlalchemy.query import Query


class UserQueryClient(Query):
    def get_by_email(self, email: str):
        if email:
            self = self.filter((User.email == email))
        return self


class User(db.Model):
    __tablename__ = 'users'
    query_class = UserQueryClient

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=True)
    last_name = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=False)
    created_at = db.Column(DateTime, nullable=False, default=lambda: datetime.utcnow())
    profile_image = db.Column(db.String, nullable=True)

    def __init__(self, first_name, last_name, email, profile_image):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.profile_image = profile_image

    def __repr__(self):
        return '<id {}>'.format(self.id)


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    first_name = fields.String()
    last_name = fields.String()
    email = fields.Email()
    profile_image = fields.URL()