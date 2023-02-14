
from config import db
from domains.user.model import User


class UserService:


    def create_user(self, first_name, last_name, email, picture):
        user = User(first_name, last_name, email, picture)
        db.session.add(user)
        db.session.commit()

        return user