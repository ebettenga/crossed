from config import db
from domains.crosswords.service import CrossWordService


from domains.room.model import Room

crossword_service = CrossWordService()


class RoomService:
    def create_room(self, user_id, crossword_id):
        room = Room(user_id, crossword_id)

        room.found_letters = crossword_service.create_found_letters_template(
            crossword_id
        )

        db.session.add(room)
        db.session.commit()

        return room

    def join_room(self, user_id, join_id):
        room: Room = Room.query.filter_by(join_id=join_id).one_or_404()

        room.player_2_id = user_id

        return room
