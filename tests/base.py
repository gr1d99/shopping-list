"""
    contains base test class for all tests
"""

from flask_testing import TestCase
from main import APP


class ShoppingListTestBase(TestCase):
    """
        Base class for all tests cases
    """
    def create_app(self):
        """
        create flask instance
        """
        app = APP
        app.testing = True
        app.debug = False
        app.secret_key = 'vhdvchvvhvdvhvjhvcjvcs'
        return app

    def setUp(self):
        """
        will be called before each test is run
        """
        self.app = self.create_app()
