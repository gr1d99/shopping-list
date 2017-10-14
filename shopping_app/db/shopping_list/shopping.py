"""Contains User, ShoppingList and ShoppingItem classes"""


class ShoppingItem(object):
    """hold shopping item details"""
    def __init__(self):
        self.name = None
        self.quantity = None
        self.price = None
        self.checked = None

    def create(self, name: str, quantity: int, price: float, checked: bool):
        if not isinstance(name, str):
            raise TypeError("Expected %(name)s to be of type `%(xtype)s" % dict(name=name, xtype=str.__name__))

        if not isinstance(price, float):
            raise TypeError("Expected %(price)s to be a float" % dict(price=price))

        if not isinstance(quantity, int):
            raise TypeError("Expected %(quantity)s to be an int" % dict(quantity=quantity))

        if not isinstance(checked, bool):
            raise TypeError("Expected %(checked)s to be a `bool`")

        self.name = name
        self.quantity = quantity
        self.price = price
        self.checked = checked
        return True

    @property
    def total_price(self):
        return self.quantity * self.price

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
    """Store shopping list details including shopping items instance"""

    def __init__(self):
        self.name = None
        self.added_by = None
        self.date_added = None
        self.items = []

    def create(self, name, added_by, date_added):
        """validates arguments and creates an instance"""
        if not isinstance(name, str):
            raise TypeError("Expected %(name)s to be an instance of `%(ins)s`" % dict(name=name, ins=str.__name__))

        if not isinstance(added_by, str):
            raise TypeError("Expected %(added_by)s to be an instance of `%(ins)s`"
                            % dict(added_by=added_by, ins=str.__name__))

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
            return True
        return

    def update(self, field, val):
        """
        Update shopping list field followed by a new val
        :param field: name
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
