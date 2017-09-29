
"""
Contains all helper functions needed to assist in performing
shopping list crud operations
"""
import os
import random
import string
import main


def secret_key_gen():
    """
    a function to generate random secret keys
    :return: random text
    """
    filepath = os.path.dirname(os.path.dirname
                               (os.path.dirname
                                (os.path.abspath(__file__)))) + '/secret.txt'
    generated_key = ''.join([random.SystemRandom().choice(string.ascii_letters + string.digits)
                             for _ in range(50)])
    with open(filepath, 'w') as secret_file:
        secret_file.write(
            '%(key)s' % dict(key=generated_key)
        )


def check_name(name):
    """
    check if a shopping list with the provided argument exists
    :param name: name of the shopping list
    :return: True or False
    """
    for shl in main.APP.shopping_list:
        if shl.get('name') == name:
            return True
    return False


def check_item(sname, iname):
    """
    check if shopping list has an item with the name provided in
    the argument.
    :param sname: shopping list name
    :param iname: item name
    :return: True or False
    """
    if check_name(sname):
        shl = get_shl(sname)
        items = shl.get('shl').items
        for item in items:
            if item.name == iname:
                return True
        return False
    return False


def get_shl(name):
    """
    Returns a shopping list
    :param name: name of the shopping list
    :return: shopping list instance
    """
    for shl in main.APP.shopping_list:
        if shl.get('name') == name:
            return shl


def get_item(shl_name, item_name):
    """
    gets a shopping item instance
    :param shl_name: shopping list name
    :param item_name: shopping item name
    :return: item instance
    """
    shl = get_shl(shl_name)
    items = shl.get('shl').items
    for item in items:
        if item.name == item_name:
            return item
    return False


def check_duplicate_item_name(shl_name, item_name):
    """
    checks if the item name already exists
    :param shl_name: shopping list name
    :param item_name: shopping item name
    :return:
    """
    for shl in main.APP.shopping_list:
        if shl.get('name') == shl_name:
            for item in shl.get('shl').items:
                if item.name == item_name:
                    return True

            return False


def change_shl_name(name, new_name):
    """
    Changes shopping list name in the main instance
    :param name: old shopping list name
    :param new_name: new shopping list name
    :return: True or False
    """
    for shl in main.APP.shopping_list:
        if shl.get('name') == name:
            shl['name'] = new_name
            return True
    return False
