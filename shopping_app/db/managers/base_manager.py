"""contains base user manager with special methods"""
from passlib.hash import pbkdf2_sha256


class BaseUserManager(object):
    """base user manager containg special methods"""
    def __init__(self):
        self.model = None

    @classmethod
    def hash_password(cls, raw_password):
        """
        never store passwords in plaintext
        :param raw_password:
        :return: hashed password
        """
        return pbkdf2_sha256.hash(raw_password)

    @classmethod
    def normalize_email(cls, email):
        """
        Normalize the email address by lowercasing the domain part of it.
        """
        email = email or ''
        try:
            email_name, domain_part = email.strip().rsplit('@', 1)
        except ValueError:
            pass
        else:
            email = '@'.join([email_name, domain_part.lower()])
        return email

    def _create_user(self, username, email, password):
        email = self.normalize_email(email)
        password = self.hash_password(password)
        self.model.__setattr__(self.model.USERNAME_FIELD, username)
        self.model.__setattr__(self.model.EMAIL_FIELD, email)
        self.model.__setattr__(self.model.PASSWORD_FIELD, password)
        return self.model
