import json
from flask import request, session

from marshmallow import ValidationError
from config import socketio
from domains.authentication.service import login_required
from domains.authentication.views import *
from domains.room.model import CreateRoomSchema, RoomSchema
from domains.room.service import RoomService

from domains.user.model import *


from config import socketio
from flask_socketio import emit, join_room, send


room_service = RoomService()


@app.route("/api/v1/rooms", methods=["POST"])
@login_required
def create_room():
    user = session["user"]
    room_payload = request.get_json()
    inbound_schema = CreateRoomSchema()

    try:
        data = inbound_schema.load(room_payload)
    except ValidationError as err:
        return err.messages, 422

    room = room_service.create_room(user.get("id"), data.get("crossword_id"))

    outbound_schema = RoomSchema()
    return outbound_schema.dump(room)


@app.route("/join_room/<int:join_id>", methods=["POST"])
@login_required
def join_user_to_room(join_id):
    user = session["user"]

    room = room_service.join_room(user.get("id"), join_id)

    return redirect(f"http://localhost:5173/join/{room.id}")


@socketio.on("connect")
def connected():
    """event listener when client connects to the server"""
    print(request.sid)
    print("client has connected")
    emit("connect", {"data": f"id: {request.sid} is connected"})


@socketio.on("join")
def on_join(data):
    room = data["room"]
    session["room"] = room
    room = join_room(room)
    print(room)
    socketio.emit("room_joined", "player has joined", to=room)


@socketio.on("message")
def handle_message(data):
    print("got message", data)
    room = data["room"]
    print("room number", room)
    """event listener when client types a message"""
    emit("message", {"message": "Hello World"}, to=session.get("room"))


@socketio.on("game_state")
def handle_message(data):
    print(session)
    emit("state", {"state": {"test_object": data}}, to=session.get("room"))


@socketio.on("disconnect")
def disconnected():
    """event listener when client disconnects to the server"""
    print("user disconnected")
    emit("disconnect", f"user {request.sid} disconnected", broadcast=True)
