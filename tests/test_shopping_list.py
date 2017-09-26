import unittest
from shopping_app.db.models import ShoppingItem, ShoppingList, User


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


class TestShoppingList(unittest.TestCase):
    def setUp(self):
        user = User()
        user.create_user('gideon', 'gideon', '')
        self.db = ShoppingList()
        self.user_instance = user.get_user('gideon')

    def test_args_validation(self):  # test whether arguments passed are validated
        self.assertRaises(TypeError, self.db.create, 1, 'user', 'today')  # test first arg
        self.assertRaises(TypeError, self.db.create, 'Cabbages', 'user', 'today')  # test second arg
        self.assertRaises(TypeError, self.db.create, 1, self.user_instance, 'today')  # test third arg

    def test_shopping_list_creation(self):
        status = self.db.create('Grocery', self.user_instance, '')
        self.assertTrue(status)

if __name__ == '__main__':
    unittest.main()
