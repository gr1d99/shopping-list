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

    def __init__(self, name):
        self.name = name
        self.items = []

    def add(self, item):
        """
        Add shopping items to the shopping list
        :return:
        """
        if not isinstance(item, ShoppingItem):

            raise TypeError("the item you added should be an instance of "
                            "%(instance)s, instead found %(errtype)s" % dict(instance=ShoppingItem.__class__,
                                                                         errtype=item.__class__.__name__))

        self.items.append(item)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "<%(name)s obj>" % dict(name=self.name)



