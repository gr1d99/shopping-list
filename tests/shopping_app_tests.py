import json
import os
import unittest

from shopping_app.core import UserAlreadyExists
from shopping_app.db import User, USERS_FILE


class TestUserModel(unittest.TestCase):
    """This test case will test the User model class"""

    def setUp(self):
        # we need to setup test db first
        self.test_db = USERS_FILE.replace('users.json', 'test_users.json')

        # remove it if it exists
        remove = lambda p: os.remove(p)
        if os.path.isfile(self.test_db):
            remove(self.test_db)

        # then initialize the db to support data entry
        with open(self.test_db, 'w') as f:
            json.dump([], f)

        # setup usernames and passwords
        username = 'Gideon'
        password = 'Password'
        self.cridentials = username, password

        # initialize user model
        self.model = User()
        self.model.db = self.test_db

    def test_usercreation(self):
        """
        Test if True is returned after user is created
        :return:
        """
        user = self.model.create_user(username=self.cridentials[0], password=self.cridentials[1])
        self.assertTrue(user)

    def test_useralready_exists(self):
        user = self.model.create_user(username=self.cridentials[0], password=self.cridentials[1])
        self.assertTrue(user)

    def tearDown(self):
        os.remove(self.test_db)

if __name__ == '__main__':
    unittest.main()