from config import app

from domains.crosswords.service import CrossWordService

with app.app_context():
    CrossWordService().load_crosswords()
