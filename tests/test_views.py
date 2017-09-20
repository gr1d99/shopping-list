import unittest
from shopping_app import app


class ViewsTest(unittest.TestCase):
    """
    This testcase will is a passing test and it will test if the status
    code of the response returned is 200 OK
    """

    def setUp(self):
        self.app = app.test_client()

    def test_views(self):
        index = self.app.get('/')
        dashboard = self.app.get('/dashboard')
        login = self.app.get('/login')
        register = self.app.get('/register')

        self.assertEqual(index.status_code, 200)
        self.assertEqual(dashboard.status_code, 200)
        self.assertEqual(login.status_code, 200)
        self.assertEqual(register.status_code, 200)
        self.assertEqual(1, 2)
