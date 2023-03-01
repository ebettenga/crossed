from typing import Union
from flask import session
from config import db
from domains.authentication.guards import get_bearer_token_from_request
from domains.authentication.service import Auth0Service
from domains.user.model import User


class UserService:
    def get_user_by_email(self, email: str) -> Union[User, None]:
        return User.query.filter_by(email=email).one_or_none()

    def create_user(self, first_name, last_name, email, picture):
        user = User(first_name, last_name, email, picture)
        db.session.add(user)
        db.session.commit()

        return user
