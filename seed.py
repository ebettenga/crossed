from config import app

from domains.crosswords.service import CrossWordService


def seed():
    with app.app_context():
        CrossWordService().load_crosswords()
        print("Seed completed") 


if __name__ == "__main__":
    seed()