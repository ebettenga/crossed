import os

from dotenv import find_dotenv, load_dotenv
from flask import Flask
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from authlib.integrations.flask_client import OAuth
from flask_cors import CORS
from gevent import monkey

monkey.patch_all()


from domains.authentication.service import auth0_service

basedir = os.path.abspath(os.path.dirname(__file__))

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)


app = Flask(__name__)
CORS(
    app,
    origins=[
        "http://localhost:5173",
        "https://ebettenga.jprq.live",
        "https://crossed-frontend-production.up.railway.app",
    ],
)
app.secret_key = os.getenv("APP_SECRET_KEY")
## container
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "SQLALCHEMY_DATABASE_URI", "postgresql://postgres:secret@localhost:5432/crossed_db"
)

client_origin_url = os.environ.get("CLIENT_ORIGIN_URL")
auth0_audience = os.environ.get("AUTH0_AUDIENCE")
auth0_domain = os.environ.get("AUTH0_DOMAIN")

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
oauth = OAuth(app)

socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")
migrate = Migrate(app, db, compare_type=True)

auth0_service.initialize(auth0_domain, auth0_audience)


@app.after_request
def add_headers(response):
    response.headers["X-XSS-Protection"] = "0"
    response.headers["Cache-Control"] = "no-store, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    return response


class Config(object):
    DEBUG = True
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = "this-really-needs-to-be-changed"


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
