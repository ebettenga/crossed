import os

from dotenv import find_dotenv, load_dotenv
from flask import Flask
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from authlib.integrations.flask_client import OAuth


basedir = os.path.abspath(os.path.dirname(__file__))

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)


async_mode = None

if async_mode is None:
    try:
        import eventlet

        async_mode = "eventlet"
    except ImportError:
        pass

    if async_mode is None:
        try:
            from gevent import monkey

            async_mode = "gevent"
        except ImportError:
            pass

    if async_mode is None:
        async_mode = "threading"

    print("async_mode is " + async_mode)

# monkey patching is necessary because this application uses a background
# thread
if async_mode == "eventlet":
    import eventlet

    eventlet.monkey_patch()
elif async_mode == "gevent":
    from gevent import monkey

    monkey.patch_all()


app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET_KEY")
## container
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "SQLALCHEMY_DATABASE_URI", "postgresql://postgres:secret@localhost:5432/crossed_db"
)


app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode=async_mode)
oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=os.getenv("AUTH0_CLIENT_ID"),
    client_secret=os.getenv("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{os.getenv("AUTH0_DOMAIN")}/.well-known/openid-configuration',
)
migrate = Migrate(app, db, compare_type=True)


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
