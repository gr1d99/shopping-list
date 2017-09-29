"""Management module to allow addition of custom commands"""

from flask_script import Manager
from main import APP
from shopping_app.utils.helpers import secret_key_gen

MANAGER = Manager(APP)


@MANAGER.command
def generate_secret():
    """
    generate random secret
    :return: random text
    """
    secret_key_gen()


if __name__ == "__main__":
    MANAGER.run()
