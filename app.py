from config import socketio, app
from domains.results.view import *


if __name__ == '__main__':
    socketio.run(app)
