import six
import abc

"""Contains the base classes of User, Authentication and Shopping classes"""


class BaseUser(six.with_metaclass(abc.ABCMeta)):
    """
    Base User class that will provide all fuctionalities needed by the User Class.
    All methods defined here must be implemented on all classes that inherit from this class
    """
    @abc.abstractmethod
    def create_user(self, username, password):
        pass

    @abc.abstractmethod
    def get_user(self, username):
        pass

    @abc.abstractmethod
    def authenticate(self, username, password):
        pass


class BaseAuth(six.with_metaclass(abc.ABCMeta)):
    """"""
    @abc.abstractmethod
    def login(self, user):
        pass

    @abc.abstractmethod
    def logout(self, user):
        pass

    @abc.abstractmethod
    def is_authenticated(self, user):
        pass


class BaseShopping(six.with_metaclass(abc.ABCMeta)):
    """
    Base Shopping Class that will handle shopping functionalities .
    All methods defined here must also be implemented by the iheriting classes
    """
    @abc.abstractmethod
    def create_shopping_list(self, user, name, category, date_added, items):
        pass

    @abc.abstractmethod
    def filter_user_shopping_list(self, user, name=None, category=None):
        pass

    @abc.abstractmethod
    def all(self):
        pass

    @abc.abstractmethod
    def delete_shopping_list(self, user, name):
        pass

