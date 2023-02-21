from config import app


@app.route("/me")
def get_user():
    return "Hello"
