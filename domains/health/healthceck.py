from config import app


@app.route("/api/v1/healthcheck")
def healthcheck():
    return "ok"
