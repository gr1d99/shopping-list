"""contains main user classes with special methods"""


class UserDb(object):
    """Contain User details"""
    def __init__(self):
        self.username = None
        self.password = None
        self.email = None

    def __repr__(self):
        return "<%(name)s obj>" % dict(name=self.username)

    def __str__(self):
        return self.__repr__()


class BaseUser(object):
    """
    Handles validation and saving of user details
    """
    def __init__(self):
        self.user = UserDb()

    def _validate_email(self, email):
        """lowercase the domain part"""
        email = email or ''
        try:
            email_name, domain_part = email.strip().rsplit('@', 1)
        except ValueError:
            pass
        else:
            email = '@'.join([email_name, domain_part.lower()])
        return email

    def _create_user(self, username, password, email):
        username = username
        password = password
        clean_email = self._validate_email(email=email)
        return self.save(username=username, password=password, email=clean_email)

    def save(self, **details):
        """
        create an instance of user details
        :param details: keyword arguments
        :return: user instance
        """
        username = details.pop('username')
        password = details.pop('password')
        email = details.pop('email')
        self.user.username = username
        self.user.password = password
        self.user.email = email
        return self.user
