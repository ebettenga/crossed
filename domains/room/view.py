from flask import request, session

from marshmallow import ValidationError
from config import socketio, app
from domains.room.model import JoinRoomSchema, Room, RoomSchema, SubmitSquareSchema
from domains.room.service import RoomService

from domains.user.model import *


from config import socketio
from flask_socketio import emit, join_room


room_service = RoomService()


@app.route("/test", methods=["POST"])
def test():
    data = request.get_json()
    coordinates = {"x": data["x"], "y": data["y"]}

    room = room_service.guess(
        data["room_id"], coordinates, data["guess"], data["user_id"]
    )

    outbound_schema = RoomSchema()

    return outbound_schema.dump(room)


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
        emit("error", e.messages, to=request.sid)

    room: Room = room_service.join_room(data["user_id"], data["difficulty"])
    session["room"] = room.id
    join_room(room)

    outbound_schema = RoomSchema()

    emit("room_joined", outbound_schema.dump(room), to=room)


@socketio.on("message")
def handle_message(data):
    room_id = session.get("room")
    inbound_schema = SubmitSquareSchema()

    try:
        data = inbound_schema.load(data)
    except ValidationError as e:
        emit("error", e.messages, to=request.sid)

    coordinates = {"x": data["x"], "y": data["y"]}

    room = room_service.guess(room_id, coordinates, data["guess"], data["user_id"])

    outbound_schema = RoomSchema()
    emit("message", {"message": outbound_schema.dump(room)}, to=room_id)


@socketio.on("game_state")
def handle_message(data):
    print(session)
    emit("state", {"state": {"test_object": data}}, to=session.get("room"))


@socketio.on("disconnect")
def disconnected():
    """event listener when client disconnects to the server"""
    print("user disconnected")
    emit("disconnect", f"user {request.sid} disconnected", broadcast=True)
