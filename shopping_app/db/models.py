class ShoppingItem(object):
    def __init__(self, name: str, price: float, checked: bool):
        self.name = name
        self.price = price
        self.checked = checked

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

    def __init__(self, name: str, date_added: str):
        self.name = name
        self.date_added = date_added
        self.items = []

    def add(self, *args):
        """
        Add shopping items to the shopping list
        :return:
        """
        if len(args) > 0:
            for item in args:
                self.items.append(item.__dict__)
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

