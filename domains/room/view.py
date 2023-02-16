from flask import request
from config import socketio
from domains.authentication.views import *

from domains.user.model import *


from config import socketio
from flask_socketio import emit, join_room, send


@socketio.on("connect")
def connected():
    """event listener when client connects to the server"""
    print(request.sid)
    print("client has connected")
    emit("connect", {"data": f"id: {request.sid} is connected"})


@socketio.on("join")
def on_join(data):
    username = data["username"]
    room = data["room"]
    join_room(room)
    print(room)
    send(username + " has entered the room.", to=room)


@socketio.on("emit")
def on_join(data):
    username = data["username"]
    room = data["room"]
    join_room(room)
    print(room)
    send("Everybody do the flop", to=room)


@socketio.on("game")
def handle_message(data):
    """event listener when client types a message"""
    room = data["room"]
    join_room(room)
    print(room)
    print("data from the front end: ", str(data))
    send({"data": data, "id": request.sid}, to=room)


@socketio.on("disconnect")
def disconnected():
    """event listener when client disconnects to the server"""
    print("user disconnected")
    emit("disconnect", f"user {request.sid} disconnected", broadcast=True)
