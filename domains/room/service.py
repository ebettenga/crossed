from config import db


from domains.room.model import Room


class RoomService:
    def create_room(self, user_id, crossword_id):
        room = Room(user_id, crossword_id)

        db.session.add(room)
        db.session.commit()

        return room
