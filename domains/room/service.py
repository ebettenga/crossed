from config import db
from domains.crosswords.model import Crossword
from domains.crosswords.service import CrossWordService


from domains.room.model import Room

crossword_service = CrossWordService()


class RoomService:
    def join_room(self, user_id, difficulty):
        room = self.find_empty_room_by_difficulty(difficulty)

        if room:
            room = self.join_existing_room(room, user_id)
        else:
            room = self.create_room(user_id, difficulty)

        return room

    def join_existing_room(self, room, user_id):
        room.player_2_id = user_id
        return room

    def create_room(self, user_id, difficulty):
        crossword = crossword_service.get_crossword_by_difficulty(difficulty)

        room = Room(user_id, crossword.id, difficulty)

        room.found_letters = crossword_service.create_found_letters_template(
            crossword.id
        )

        db.session.add(room)
        db.session.commit()

        return room

    def find_empty_room_by_difficulty(self, difficulty):
        return (
            Room.query.filter_by(player_2_id=None, difficulty=difficulty)
            .order_by(Room.created_at)
            .first()
        )
