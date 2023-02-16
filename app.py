from config import socketio, app
from domains.authentication.views import *
from domains.room.view import *
from domains.crosswords.view import *
from domains.user.model import *
from domains.crosswords.model import *


from config import socketio


if __name__ == "__main__":
    socketio.run(app)
