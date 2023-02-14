from config import socketio, app
from domains.results.view import *
from domains.authentication.views import *

if __name__ == '__main__':
    socketio.run(app)
