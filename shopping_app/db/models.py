import json
import os
from .base import BaseShopping, BaseUser
from ..core.exceptions import UserAlreadyExists, UserDoesNotExist

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

SHOPPING_FILE = os.path.join(BASE_PATH, 'datastore/data.json')
USERS_FILE = os.path.join(BASE_PATH, 'datastore/users.json')


class ShoppingList(BaseShopping):
    """A class model that will handle creation of shopping_list of users"""

    def __init__(self):
        self.db = SHOPPING_FILE

    def create_shopping_list(self, user, name, category, date_added, items):

        # we will first check if the shopping list of the same user with the same
        # shopping_list name and category name exists.
        # if it does we will have to denie the user to add duplicate data

        new_data = {
            'shopping_list': [
                {
                    'user': user,
                    'shopping_list_name': name,
                    'category': category,
                    'date_added': date_added,
                    'items': items
                }
            ]
        },

        # check if file exists

        if os.path.isfile(SHOPPING_FILE):
            with open(SHOPPING_FILE, 'r') as f:
                old_data = json.load(f)
                old_data.append(new_data[0])

            with open(SHOPPING_FILE, 'w') as f:
                json.dump(old_data, f, indent=2, separators=(',', ': '))
                return True  # that is if data is written successfully

        return  # if nothing happens

    def filter_user_shopping_list(self, user, name=None, category=None):
        """we will only check if user exists in the available in the shopping list"""
        results = None

        if os.path.isfile(SHOPPING_FILE):
            with open(SHOPPING_FILE, 'r') as f:
                data = json.load(f)

            def get_user(dct):  # fetch user
                usr = dct.get('shopping_list')[0].get('user')
                return usr

            def get_name(dct):  # fetch shopping_list name
                usr = dct.get('shopping_list')[0].get('shopping_list_name')
                return usr

            def get_category(dct):  # fetch category name
                usr = dct.get('shopping_list')[0].get('category')
                return usr

            if not name and not category:  # return only results queried with user
                results = [l for l in data if user == get_user(l)]

            if name and not category:  # return results queried with user and shopping_list name
                results = [l for l in data if (user == get_user(l) and name == get_name(l))]

            if not name and category:  # return results queried with user and category
                results = [l for l in data if (user == get_user(l) and category == get_category(l))]

            if name and category:  # return results queried with extra keywords
                results = [l for l in data if (user == get_user(l) and name == get_name(l) and category == get_category(l))]

            return results

    def all(self):
        """
        fetch all shopping lists
        :return:
        """
        if os.path.isfile(SHOPPING_FILE):
            with open(SHOPPING_FILE, 'r') as f:
                data = json.load(f)
            return data
        return []

    def delete_shopping_list(self, user, name):
        """
        Deleting a shopping list is simple now, we only need to query using
        two unique keys for each shopping list, name and user
        :param user:
        :param name:
        :return: True if deletion was successful
        """

        # get the exact list to be deleted
        target_shl = self.filter_user_shopping_list(user, name=name)[0]
        # lets first get the whole shopping list
        if os.path.isfile(SHOPPING_FILE):
            with open(SHOPPING_FILE, 'r') as f:
                shl = json.load(f)

            shl.remove(target_shl)
            if True:
                with open(SHOPPING_FILE, 'w') as f:
                    json.dump(shl, f, indent=2, separators=(',', ': '))
                return True


class User(BaseUser):
    """
    User class that will create users
    """

    def __init__(self):
        self.db = USERS_FILE

    def create_user(self, username, password):

        # but we first need to validate if the username already exists
        if not self.check_user(username):

            new_data = {
                'user': {
                    'username': username,
                    'password': password
                }
            }

            if os.path.isfile(self.db):  # check if file exists
                with open(self.db, 'r') as f:
                    old_data = json.load(f)
                    old_data.append(new_data)

                with open(self.db, 'w') as f:
                    json.dump(old_data, f, indent=2, separators=(',', ': '))
                    return True  # that is if data is written successfully

            return  # if nothing happens

        raise UserAlreadyExists

    def check_user(self, username):
        if os.path.isfile(self.db):  # check if file exists
            with open(self.db, 'r') as f:
                all_users = json.load(f)

            allusers = (user for user in all_users)  # user a generator since it is faster
            usernames = [user.get('user').get('username') for user in allusers]
            if username in usernames:
                return True

            return False

    def get_user(self, username):
        if os.path.isfile(self.db):  # check if file exists
            with open(self.db, 'r') as f:
                all_users = json.load(f)

            for user in all_users:
                if user.get('user').get('username') == username:
                    return user
            raise UserDoesNotExist

    def authenticate(self, username, password):
        if os.path.isfile(self.db):  # check if file exists
            with open(self.db, 'r') as f:
                all_users = json.load(f)

            for user in all_users:
                if user.get('user').get('username') == username and user.get('user').get('password') == password:
                    return True
            return False
