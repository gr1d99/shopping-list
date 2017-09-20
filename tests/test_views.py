from flask_testing import TestCase
from shopping_app import app


class ShoppingAppTest(TestCase):

    """This TestCase will test various functionalities of the application"""
    def create_app(self):
        app.config['TESTING'] = True
        return app

    # ----------TemplatesTest------------- #

    def test_index_template(self):
        """
        test whether the index.html template is the one used
        :return: True, False
        """
        app.test_client().get('/')
        self.assert_template_used('index.html')

    def test_login_template(self):
        """
        test whether the login.html template is the one used
        :return: True, False
        """
        app.test_client().get('/login')
        self.assert_template_used('login.html')

    def test_dashboard_template(self):
        """
        test whether the index.html template is the one used
        :return: True, False
        """
        app.test_client().get('/dashboard')
        self.assert_template_used('dashboard.html')

    def test_register_template(self):
        """
        test whether the register.html template is the one used
        :return: True, False
        """
        app.test_client().get('/register')
        self.assert_template_used('dashboard.html')



