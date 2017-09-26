import unittest
from shopping_app.core.exceptions import UserDoesNotExist
from shopping_app.db.models import User


class TestUser(unittest.TestCase):
    """A class to test user class"""
    def setUp(self):
        self.db = User()
        self.user_details = {'username': 'Gideon', 'password': 'password123', 'email': ''}

    def test_user_creation(self):
        """
        test whether the user is created
        :return: True
        """
        self.db.create_user(
            self.user_details.get('username'),
            self.user_details.get('password'),
            self.user_details.get('email')
        )
        self.assertTrue(self.db.check_user(self.user_details.get('username')))

    def test_user_who_doesnt_exist(self):
        """test whether an exception is raised when user does not exist"""
        self.assertRaises(UserDoesNotExist, self.db.get_user, 'anon')

    def test_user_validation(self):
        self.db.create_user(
            self.user_details.get('username'),
            self.user_details.get('password'),
            self.user_details.get('email')
        )
        self.assertFalse(self.db.validate_user('admin', '123'))  # a user who does not exist
        self.assertTrue(self.db.validate_user('Gideon', 'password123'))  # test user who exists

if __name__ == '__main__':
    unittest.main()
