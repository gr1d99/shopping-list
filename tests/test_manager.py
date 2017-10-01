"""Test all managers"""

import unittest
from model.managers.manager import UserManager
from model.user import User


class TestUserManager(unittest.TestCase):
    """test all methods and attributes of UserManager class"""

    def setUp(self):
        """create UserManager instance and make it available to the test case class"""
        self.manager = UserManager()
        self.user_details = {'username': 'Gideon',
                             'email': 'gideon@gmail.com',
                             'password': 'gideonpassword'}

    def test_user_attribute_is_instance_of_user_class(self):
        """
        manager user attribute should be an instance of User class
        :return:
        """
        self.assertTrue(isinstance(self.manager.model, User))

    def test_create_user_without_username(self):
        """
        assert an exception is raised
        :return:
        """
        self.assertRaises(ValueError,
                          self.manager.create_user,
                          email='gideon@gmail.com',
                          password='gideon')

    def test_create_user_without_password(self):
        """
        assert an exception is raised
        :return:
        """
        self.assertRaises(ValueError,
                          self.manager.create_user,
                          username='gideon',
                          email='gideon@gmail.com')

    def test_create_user(self):
        """
        test if user is created successfully and a user instance is returned
        :return:
        """
        user_details = self.user_details
        user = self.manager.create_user(
            username=user_details.pop('username'),
            email=user_details.pop('email'),
            password=user_details.pop('password')
        )
        self.assertIsInstance(user, User)

    def test_hash_password(self):
        """
        test if the hashed password is equal to raw password
        :return:
        """
        password = 'password'
        self.assertNotEqual(self.manager.hash_password(password), password)

    def test_verify_password(self):
        user_details = self.user_details
        user = self.manager.create_user(
            username=user_details.pop('username'),
            email=user_details.pop('email'),
            password=user_details.pop('password')
        )
        self.assertTrue(user.verify_password('gideonpassword'))
