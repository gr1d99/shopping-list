from flask_testing import TestCase
from main import APP


class ShoppingListTestBase(TestCase):
    def create_app(self):
        app = APP
        app.testing = True
        app.debug = False
        app.secret_key = 'vhdvchvvhvdvhvjhvcjvcs'
        return app

    def setUp(self):
        self.app = self.create_app()
