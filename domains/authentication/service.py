


from functools import wraps

from flask import session


def login_required(function):
    @wraps(function)
    def decorated_func(*args, **kwargs):
        if session.get("user"):
            return function(*args, **kwargs)
        else:
            return {"message": "login required"}, 403
    return decorated_func
