class UserDb(object):
    def __init__(self):
        self.username = None
        self.password = None
        self.email = None

    def __repr__(self):
        return "<%(name)s obj>" % dict(name=self.username)

    def __str__(self):
        return self.__repr__()


class BaseUser(object):
    def __init__(self):
        self.db = UserDb()

    def _validate_email(self, email):  # thanks Django
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
        username = details.pop('username')
        password = details.pop('password')
        email = details.pop('email')
        self.db.username = username
        self.db.password = password
        self.db.email = email
        return self.db
