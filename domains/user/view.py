from config import app
from flask import g, request
from domains.authentication.guards import authorization_guard
from domains.user.model import UserSchema
from domains.user.service import UserService

user_service = UserService()


@app.route("/api/v1/me", methods=["POST"])
@authorization_guard
def get_user():
    user_data = request.get_json()

    user = user_service.get_user_by_email(user_data["email"])

    if not user:
        user = user_service.create_user(
            user_data["name"],
            user_data["family_name"],
            user_data["email"],
            user_data["picture"],
        )

    outbound_mapper = UserSchema()

    return outbound_mapper.dump(user)
