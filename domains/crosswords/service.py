import datetime
import json
import os
import re
from config import db
from flask_sqlalchemy.query import Query
from domains.crosswords.model import Crossword
from sqlalchemy.sql.expression import func

from domains.room.model import Room


class CrossWordService:
    def __init__(self):
        pass

    def get_crosswords(self, page, limit, dow, col_size, row_size):
        crosswords: Query = Crossword.query

        if dow:
            crosswords = crosswords.filter_by(dow=dow)

        if col_size:
            crosswords = crosswords.filter_by(col_size=col_size)

        if row_size:
            crosswords = crosswords.filter_by(row_size=row_size)

        crossword_pagination = crosswords.paginate(page=page, per_page=limit)
        return crossword_pagination

    def load_crosswords(self):
        for root, dirs, files in os.walk("./crosswords"):
            for file in files:
                with open(root + "/" + file) as f:
                    try:
                        data = json.load(f)
                        date = datetime.datetime.strptime(data["date"], "%m/%d/%Y")
                        del data["date"]
                        data["col_size"] = data["size"]["cols"]
                        data["row_size"] = data["size"]["rows"]

                        if data["shadecircles"] in ["true", "false"]:
                            if data["shadecircles"] == "true":
                                data["shadecircles"] = True
                            else:
                                data["shadecircles"] = False

                        crossword = Crossword(**data, date=date)
                        db.session.add(crossword)
                        db.session.commit()
                    except TypeError as e:
                        print(f"{root}/{file} got a type error :(")
                        db.session.rollback()
                    except Exception as e:
                        db.session.rollback()
                        print(f"{root}/{file} could not be parsed using json")
                        print(e)

    def create_found_letters_template(self, crossword_id):
        crossword: Crossword = Crossword.query.get(crossword_id)

        return [re.sub("[A-Za-z]", "*", v) for v in crossword.grid]

    def get_crossword_by_difficulty(self, difficulty: str) -> Crossword:
        if difficulty.lower() == "easy":
            days = ["Monday", "Tuesday"]
        elif difficulty.lower() == "medium":
            days = ["Wednesday", "Thursday"]
        elif difficulty.lower() == "hard":
            days = ["Friday", "Saturday"]
        else:
            raise ValueError("not a correct difficulty")

        return (
            Crossword.query.filter(Crossword.dow.in_(days))
            .filter(
                Crossword.date
                > datetime.datetime.now() - datetime.timedelta(days=10 * 365)
            )
            .order_by(func.random())
            .first()
        )

    def create_answer_board(self, crossword: Crossword):
        answer_board = []
        for r in range(crossword.col_size):
            row_start = r * crossword.row_size
            answer_board.append(
                crossword.grid[row_start : row_start + crossword.row_size]
            )

        return answer_board

    def check_guess(self, room: Room, coordinates: dict, guess: str):
        crossword = room.crossword

        board = self.create_answer_board(crossword)

        return board[coordinates["x"]][coordinates["y"]] == guess.upper()
