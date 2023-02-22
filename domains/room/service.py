from config import db
from domains.crosswords.model import Crossword
from domains.crosswords.service import CrossWordService
from sqlalchemy.orm.attributes import flag_modified

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
        flag_modified(room, "player_2_id")
        db.session.merge(room)
        db.session.flush()
        db.session.commit()
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

    def guess(self, room_id: int, coordinates: dict, guess: str, user_id):
        room: Room = Room.query.get(room_id)
        is_correct = crossword_service.check_guess(room, coordinates, guess)

        if is_correct:
            self.add_points(room, user_id)
            self.update_found_board(room, coordinates, guess)
            return room
        else:
            self.remove_points(room, user_id)
            return room

    def update_found_board(self, room: Room, coordinates, guess):
        if coordinates["x"] == 0:
            x_number = 0
        else:
            x_number = coordinates["x"] * room.crossword.row_size

        space = x_number + coordinates["y"]
        room.found_letters[space] = guess
        flag_modified(room, "found_letters")
        db.session.merge(room)
        db.session.flush()
        db.session.commit()

    def add_points(self, room: Room, user_id):
        if room.player_1_id == user_id:
            room.player_1_score += 3
        else:
            room.player_2_score += 3

    def remove_points(self, room: Room, user_id):
        if room.player_1_id == user_id:
            room.player_1_score -= 1
        else:
            room.player_2_score -= 1
        # TODO: why do we need these flag_modified lines? it won't update consistently without
        flag_modified(room, "player_1_score")
        flag_modified(room, "player_2_score")
        db.session.merge(room)
        db.session.flush()
        db.session.commit()
