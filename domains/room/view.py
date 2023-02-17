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
def join_room(join_id):
    user = session["user"]

    room = room_service.join_room(user.get("id"), join_id)

    return redirect(f"http://localhost:5173/join/{room.id}")


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

    """
        Steps for playing a game
        1. user 1 picks a crossword
        2. user 1 gets a join id, which they can pass to other users
        3. user 1 joins a roomsocket
        4. user 2 hits endpoint sent to them to join the room
        5. user 2 gets redirected to the website, which grabs the room id from the path
        6. user 2 joins the roomsocket
        7. since two players have now joined the room, a message is emitted to the room telling the game to start
        8. the game starts


        Steps while playing
        1. user 1 submits room_number, col, row, and letter guessed throught the socket
        2. server checks that the letter hasn't been guessed before, and determines whether it's correct
        3. server updates the players scores and emits the new scores, if the guess was correct, it also emits the found letters
    """

    def on_join(data):
        username = data["username"]
        room = data["room"]
        join_room(room)
        print(room)
        send(username + " has entered the room.", to=room)

    def on_game(self, data):
        """event listener when client types a message"""
        room = data["room"]
        join_room(room)
        print(room)
        print("data from the front end: ", str(data))
        send({"data": data, "id": request.sid}, to=room)


socketio.on_namespace(RoomNamespace("/"))
