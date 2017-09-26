from flask_script import Manager
from main import app
from shopping_app.utils.helpers import secret_key_gen

manager = Manager(app)


@manager.command
def generate_secret():
    secret_key_gen()


if __name__ == "__main__":
    manager.run()

