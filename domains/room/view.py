import json
from flask import request, session

from marshmallow import ValidationError
from config import socketio
from domains.authentication.service import login_required
from domains.authentication.views import *
from domains.room.model import JoinRoomSchema, Room, RoomSchema
from domains.room.service import RoomService

from domains.user.model import *


from config import socketio
from flask_socketio import emit, join_room


room_service = RoomService()


@socketio.on("connect")
def connected():
    """event listener when client connects to the server"""
    print(request.sid)
    print("client has connected")
    emit("connect", {"data": f"id: {request.sid} is connected"})


@socketio.on("join")
def on_join(data):
    inbound_schema = JoinRoomSchema()

    try:
        data = inbound_schema.load(data)
    except ValidationError as e:
        return e.messages, 422

    room: Room = room_service.join_room(data["user_id"], data["difficulty"])
    session["room"] = room.id
    join_room(room)

    outbound_schema = RoomSchema()

    emit("room_joined", outbound_schema.dump(room), to=room)


@socketio.on("message")
def handle_message(data):
    print("got message", data)
    room = data["room"]
    print("room number", room)
    """event listener when client types a message"""
    emit("message", {"message": data["message"]}, to=session.get("room"))


@socketio.on("game_state")
def handle_message(data):
    print(session)
    emit("state", {"state": {"test_object": data}}, to=session.get("room"))


@socketio.on("disconnect")
def disconnected():
    """event listener when client disconnects to the server"""
    print("user disconnected")
    emit("disconnect", f"user {request.sid} disconnected", broadcast=True)
