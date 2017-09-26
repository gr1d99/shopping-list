import datetime
from .base import BaseUser, UserDb
from ..core.exceptions import UserDoesNotExist


class User(BaseUser):
    """User Model"""

    def __init__(self):
        super(User, self).__init__()
        self.users = []

    def create_user(self, username, password, email):
        self.users.append(self._create_user(username, password, email))

    def check_user(self, username):
        for user in self.users:
            if getattr(user, 'username') == username:
                return True
        return False

    def get_user(self, username):
        if not self.check_user(username):
            raise UserDoesNotExist

        for user in self.users:
            if getattr(user, 'username') == username:
                return user

    def validate_user(self, username, password):
        try:
            user = self.get_user(username)
            if user.password == password:
                return True
        except UserDoesNotExist:
            return False


class ShoppingItem(object):
    def __init__(self):
        self.name = None
        self.price = None
        self.checked = None

    def create(self, name: str, price: float, checked: bool):
        if not isinstance(name, str):
            raise TypeError("Expected %(name)s to be of type `%(xtype)s" % dict(name=name, xtype=str.__name__))

        if not isinstance(price, float):
            raise TypeError("Expected %(price)s to be a float" % dict(price=price))

        if not isinstance(checked, bool):
            raise TypeError("Expected %(checked)s to be a `bool`")

        self.name = name
        self.price = price
        self.checked = checked

        return True

    def update(self, field, val):
        """
        Update shopping item field followed by a new val
        :param field: eg name, price, checked
        :param val: new value to replace old val
        :return: True if successful, False otherwise
        """
        if hasattr(self, field):
            setattr(self, field, val)
            return True
        return False

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "<%(name)s obj>" % dict(name=self.name)


class ShoppingList(object):
    """Shopping List class"""

    def __init__(self):
        self.name = None
        self.added_by = None
        self.date_added = None
        self.items = []

    def create(self, name, added_by, date_added):
        if not isinstance(name, str):
            raise TypeError("Expected %(name)s to be an instance of `%(ins)s`" % dict(name=name, ins=str.__name__))

        if not isinstance(added_by, UserDb):
            raise TypeError("Expected %(added_by)s to be an instance of `%(ins)s`"
                            % dict(added_by=added_by, ins=User.__name__))

        if not isinstance(date_added, str):
            raise TypeError("Expected %(date_added)s to be an instance of `%(ins)s`"
                            % dict(date_added=date_added, ins=str.__name__))

        self.name = name
        self.added_by = added_by
        self.date_added = date_added

        return True

    def add_items(self, *args):
        """
        Add shopping items to the shopping list
        :return:
        """
        if len(args) > 0:
            for item in args:
                if not isinstance(item, ShoppingItem):
                    raise TypeError("Expected %(item)s to be an instance of `%(ins)s" %
                                    dict(item=item, ins=ShoppingItem.__name__))
                self.items.append(item)
            return
        return

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "<%(name)s obj>" % dict(name=self.name)


class ShoppingListManager(object):
    """A manager class that will ease retrival and storage of all shopping list"""
    def __init__(self):
        self.shopping_lists = []

    def all(self):
        """
        yield all shopping lists
        :return:
        """
        return (shl for shl in self.shopping_lists)

    def add_shl(self, *args):
        for shl in args:
            self.shopping_lists.append(shl.__dict__)

        return
