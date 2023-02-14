import os
from flask_migrate import Migrate

from app import app, db

migrate = Migrate(app, db, compare_type=True)

if __name__ == '__main__':
    migrate.init_app(app, db)
