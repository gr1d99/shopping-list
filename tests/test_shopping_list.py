import unittest
from shopping_app.db.shopping_list.shopping import ShoppingItem, ShoppingList


class TestShoppingItem(unittest.TestCase):
    """This test case will test the Shopping Item model class"""

    def setUp(self):
        """called before each test is run"""
        self.item = ShoppingItem()
        self.items = {'name': 'Grocery', 'quantity': 10, 'price': 10.0, 'checked': True}

    def test_item_creation(self):
        """
            test if item is created successfully.
            create method will return True
        """
        some_item = self.item
        items = self.items
        status = some_item.create(items.pop('name'),
                                  items.pop('quantity'),
                                  items.pop('price'), items.pop('checked'))
        self.assertTrue(status)

    def test_update_method(self):
        """
            test if update method works correctly,
            returns True if successful
        """
        some_item = self.item
        items = self.items
        some_item.create(items.pop('name'), items.pop('quantity'),
                         items.pop('price'), items.pop('checked'))
        self.assertTrue(some_item.update('name', 'Cabbage'))

    def test_total_price(self):
        """
        check if total price calculation is as expected
        """
        some_item = self.item
        items = self.items
        some_item.create(items.pop('name'), 10, 100.00, items.pop('checked'))
        self.assertEqual(some_item.total_price, 1000.00)


class TestShoppingList(unittest.TestCase):
    """
    Test class for ShoppingList
    """
    def setUp(self):
        """called before each test"""
        self.db = ShoppingList()

    def test_first_arg_type_validation(self):
        """test whether the first argument is validates"""
        self.assertRaises(TypeError, self.db.create, 1, 'user', 'today')  # test for type error

    def test_second_arg_type_validation(self):
        """test whether the second argument is validates"""
        self.assertRaises(TypeError, self.db.create, 'Cabbages', 1, '19-09-2017')  # test second arg raises type error

    def test_third_arg_type_validation(self):
        """test whether the second argument is validates"""
        self.assertRaises(TypeError, self.db.create, 'Cabbages', 'Gideon', 1)  # test for type error

    def test_shopping_list_creation(self):
        """create a shopping list"""
        status = self.db.create('Grocery', 'Gideon', '19-09-2017')
        self.assertTrue(status)

    def test_update_shopping_list(self):
        """test ShoppingList updating"""
        some_list = self.db
        status = some_list.create('Grocery', 'Admin', '19-07-2017')
        some_list.update('name', 'Vegetables')
        self.assertTrue(status)

    def test_add_items(self):
        """test if items are successfully added to the shopping list"""
        some_item = ShoppingItem()
        some_item.create('Vegetable', 10, 10.0, True)
        some_list = ShoppingList()
        some_list.create('Grocery', 'Gideon', '19-09-2017')
        self.assertTrue(some_list.add_items(some_item))

    def test_raise_type_error(self):
        """test if item added to shopping list is an instance of shopping item"""
        some_list = ShoppingList()
        some_list.create('Grocery', 'Gideon', '19-09-2017')
        self.assertRaises(TypeError, some_list.add_items, 'some item')

if __name__ == '__main__':
    unittest.main()
