import os
from config import db
from urllib.parse import urlencode, quote_plus

from flask import session, redirect, url_for

from config import app, oauth
from domains.user.model import User, UserQueryClient, UserSchema
from domains.user.service import UserService


user_service = UserService()

@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    query: UserQueryClient = User.query
    user = query.get_by_email(token["userinfo"]["email"]).first()

    if not user:
        user_info: dict = token["userinfo"]
        user_service.create_user(user_info.get("given_name"), user_info.get("family_name"), user_info.get("email"), user_info.get("picture"))
        
    user_schema = UserSchema()
    session["user"] = user_schema.dump(user)
    return user_schema.dump(user)


@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://"
        + os.getenv("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "client_id": os.getenv("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )