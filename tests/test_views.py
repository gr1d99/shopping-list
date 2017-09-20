from flask_testing import TestCase
from shopping_app import app


class ShoppingAppTest(TestCase):

    """This TestCase will test various functionalities of the application"""
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_login(self):
        resp = app.test_client.post('/login', data=dict(username='admin', password='user'))
        self.assertRedirects(resp.status_code, location='/')
