"""Contains User class"""
from .base_user import BaseUser


class User(BaseUser):
    """User class"""
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    PASSWORD_FIELD = 'password'

    def __init__(self):
        """Initialize class attributes"""
        # set all attributes to None because we will validate first
        # before assigning values
        self.username = None
        self.email = None
        self.password = None

    @property
    def get_username(self):
        """
        gets username value
        :return:
        """
        return getattr(self, User.USERNAME_FIELD)

    @property
    def get_email(self):
        """
        gets email value
        :return:
        """
        return getattr(self, User.EMAIL_FIELD)

    def verify_password(self, password):
        """verify provided password with the stored password"""
        return self._verify_password(password)

    def __str__(self):
        return '<%(username)s obj>' % dict(username=self.get_username)

    def __repr__(self):
        return self.__str__()