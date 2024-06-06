import os
from config import socketio, app
from domains.room.view import *
from domains.crosswords.view import *
from domains.user.view import *
from domains.user.model import *
from domains.crosswords.model import *
from domains.room.model import *
from domains.health.healthceck import *
from migrations.run_migrations import run_migrations

print("Starting Server")
print(f"PORT: {os.getenv('PORT', 5000)}")
socketio.run(
    app, host="0.0.0.0", port=os.getenv("PORT", 5000), allow_unsafe_werkzeug=True
)
