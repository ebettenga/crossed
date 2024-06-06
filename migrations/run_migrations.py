import os
from seed import seed
from alembic.config import Config
from alembic import command
def run_migrations():
    # Run your migrations using Alembic
    print("Running migrations")
    alembic_cfg = Config("./migrations/alembic.ini")  # Replace with your Alembic configuration file path
    command.upgrade(alembic_cfg, "head")
    seed()

if __name__ == "__main__":
    run_migrations()
    print("Migrations complete.")