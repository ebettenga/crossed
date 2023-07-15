import os
from config import socketio, app
from domains.room.view import *
from domains.crosswords.view import *
from domains.user.view import *
from domains.user.model import *
from domains.crosswords.model import *
from domains.room.model import *
from domains.health.healthceck import *

from config import socketio


print("Starting Server")
print(f"PORT: {os.getenv('PORT', 5000)}")
socketio.run(app, port=os.getenv("PORT", 5000))
