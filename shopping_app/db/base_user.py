"""base class for User class"""

from passlib.hash import pbkdf2_sha256


class BaseUser(object):
    """base user class with special methods"""
    def _verify_password(self, password):
        return pbkdf2_sha256.verify(password, getattr(self, self.PASSWORD_FIELD))
