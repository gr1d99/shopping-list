"""Contains all tests for the User class"""


import unittest
from shopping_app.db.user import User


class TestUser(unittest.TestCase):
    """Tests all initial attributes and methods"""

    def setUp(self):
        """initialize User class and make it available to the test class"""
        self.user = User()

    def test_has_username_field(self):
        """
        assert whether User class has attribute USERNAME_FIELD
        :return:
        """
        self.assertTrue(hasattr(self.user, 'USERNAME_FIELD'))

    def test_has_email_field(self):
        """
        assert if User class has attribute EMAIL_FIELD
        :return:
        """
        self.assertTrue(hasattr(self.user, 'EMAIL_FIELD'))

    def test_has_password_field(self):
        """
        assert if User class has PASSWORD_FIELD
        :return:
        """
        self.assertTrue(hasattr(self.user, 'PASSWORD_FIELD'))

    def test_username_default_is_none(self):
        """
        assert if User instance attribute username default value is None
        :return:
        """
        self.assertTrue(getattr(self.user, self.user.USERNAME_FIELD) is None)

    def test_email_default_is_none(self):
        """
        assert if User instance attribute email default value is None
        :return:
        """
        self.assertTrue(getattr(self.user, self.user.EMAIL_FIELD) is None)

    def test_password_default_is_none(self):
        """
        assert if User instance attribute password default value is None
        :return:
        """
        self.assertTrue(getattr(self.user, self.user.PASSWORD_FIELD) is None)

    def test_username_is_none(self):
        """
        assert get_username method returns a None
        :return:
        """
        self.assertIsNone(self.user.get_username)

    def test_get_email_is_none(self):
        """
        assert get_email method returns a None
        :return:
        """
        self.assertIsNone(self.user.get_email)
