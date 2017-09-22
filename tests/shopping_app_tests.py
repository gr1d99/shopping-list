import unittest
from shopping_app.db import ShoppingItem


class TestShoppingItem(unittest.TestCase):
    """This test case will test the User model class"""

    def setUp(self):
        self.db = ShoppingItem
        self.items = {'name': 'Grocery', 'price': 10.0, 'checked': True}
        self.model_attributes = ['update']

    def test_model_attributes(self):
        for attr in self.model_attributes:
            self.assertTrue(hasattr(self.db, attr))

    def test_is_of_class_type(self):
        self.assertTrue(isinstance(self.db, type))

    def tearDown(self):
        del self.db
        del self.items


if __name__ == '__main__':
    unittest.main()