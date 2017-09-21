from db.models import SHOPPING_FILE, USERS_FILE
import json
from flask_script import Manager
from shopping_app import app
from utils.helpers import secret_key_gen

manager = Manager(app)


@manager.command
def generate_secret():
    secret_key_gen()

@manager.command
def resetdb():
    files = [SHOPPING_FILE, USERS_FILE]
    for file in files:
        with open(file, 'w') as f:
            json.dump([], f)


if __name__ == "__main__":
    manager.run()

