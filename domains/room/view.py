from flask import request, session
from flask_socketio import Namespace
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


@app.route("/api/v1/room", methods=["POST"])
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


class RoomNamespace(Namespace):
    def on_connect(self):
        print(session)
        """event listener when client connects to the server"""
        print(request.sid)
        print("client has connected")
        emit("connect", {"data": f"id: {request.sid} is connected"})

    def on_disconnect(self):
        """event listener when client disconnects to the server"""
        print("user disconnected")
        emit("disconnect", f"user {request.sid} disconnected", broadcast=True)

    def on_error(self, e):
        print(request.event["message"])  # "my error event"
        print(request.event["args"])
        print(e)

    def on_game(self, data):
        """event listener when client types a message"""
        room = data["room"]
        join_room(room)
        print(room)
        print("data from the front end: ", str(data))
        send({"data": data, "id": request.sid}, to=room)

    def on_join(data):
        username = data["username"]
        room = data["room"]
        join_room(room)
        print(room)
        send(username + " has entered the room.", to=room)


socketio.on_namespace(RoomNamespace("/"))
