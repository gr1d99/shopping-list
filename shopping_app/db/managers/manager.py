"""Contain User class managers"""
from ..user import User
from .base_manager import BaseUserManager


class UserManager(BaseUserManager):
    """a manager class for User class, responsible for creation of user instances"""
    def __init__(self):
        super(UserManager, self).__init__()
        self.model = User()

    def create_user(self, username=None, email=None, password=None):
        """
        create user instance but first ensure that required data is provided
        :param username:
        :param email:
        :param password:
        :return:
        """
        if not username:
            raise ValueError("%(field)s cannot be empty" % dict(field=username))

        if not password:
            raise ValueError("%(field)s cannot be empty" % dict(field=password))

        return self._create_user(username, email, password)
