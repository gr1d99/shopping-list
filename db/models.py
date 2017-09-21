

class User(BaseUser):
    def __init__(self):
        self.users = {}

    def create_user(self, username, password):
        self.add_user(username=username, password=password)

    def add_user(self, **details):
        username = details.pop('username', None)
        password = details.pop('password', None)
        if self.validate_user(username=username, password=password):
            clean_details = {'username': username, 'password': password}
            self.users.update({username: clean_details})

    def validate_user(self, **details):
        username = details.pop('username', None)
        password = details.pop('password', None)

        if not username:
            raise UsernameEmpty

        if not password:
            raise PasswordEmpty

        if username in self.users.keys():
            raise UserAlreadyExists

        return True

    def get_user(self, username):
        if username not in self.users.keys():
            raise UserDoesNotExist

        return self.users.get(username)

    #
    # def update_user(self, username):
    #     pass
    #
    # def delete_user(self, usename):
    #     pass
