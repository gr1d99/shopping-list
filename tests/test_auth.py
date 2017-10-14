"""
This module contains User and Views authentication tests
"""

import unittest
from main import APP


class TestBase(unittest.TestCase):
    """
    Base test class
    """
    def setUp(self):
        """Create instances and objects that will be used by the tests"""
        APP.testing = True
        APP.debug = False
        APP.secret_key = '123E33R44F4T4T'
        self.app = APP
        user_details = {  # a dictionary corresponding to the form fields
            'username': 'user100',
            'email': 'gideonkimutai9@gmail.com',
            'password': 'user100password',
            'confirm': 'user100password',
        }
        self.user_details = user_details

    def register(self, **options):
        """
        a helper method that posts user details
        :param options: dictionary of user details
        :return: response
        """
        return self.app.test_client().post('/register',
                                           data=dict(options),
                                           follow_redirects=True)

    def login(self, **cridentials):
        """
        a helper method to post user login cridentials
        ad return a response
        :param cridentials: username and password
        :return: response
        """
        return self.app.test_client().post('/login',
                                           data=dict(cridentials),
                                           follow_redirects=True)

    def logout(self):
        """
        A helper method to logout users
        """
        return self.app.test_client().get('/logout', follow_redirects=True)


class TestUserAuth(TestBase):
    """Test case that covers user registration and login and logout"""

    def test_user_authentication(self):

        """
        tests if user registers logins and logouts successfully.
            - we should get a status code of 200 ok
            - we should also follow redirect after registration and login so
            that we can check for success messages is in the returned data

        """

        # ----------------> START OF USER REGISTRATION <--------------- #
        reg_resp = self.register(username=self.user_details.get('username'),
                                 email=self.user_details.get('email'),
                                 password=self.user_details.get('password'),
                                 confirm=self.user_details.get('confirm'))

        self.assertEqual(reg_resp.status_code, 200)
        self.assertIn(b'Success! you may now login using your username and password', reg_resp.data)
        # ---------------> END OF USER REGISTRATION <------------------ #

        # --------------> START OF USER LOGIN <----------- #
        login_resp = self.login(username=self.user_details.get('username'),
                                password=self.user_details.get('password'))
        self.assertEqual(login_resp.status_code, 200)
        self.assertIn(b'Success!! you are now logged in', login_resp.data)
        # --------------> END OF USER LOGIN <------------- #

        # --------------> START OF USER LOGOUT <-----------#
        logout_resp = self.logout()
        self.assertIn(b'successfully logged out!', logout_resp.data)
        # --------------> END OF USER LOGOUT <-----------#


class TestViewsAuthentication(TestBase):
    """
    test class to test if views requiring user authentication
    are properly handles un-authenticated requests
    """
    def test_views_authentication(self):
        """
        test for views that require user authentication
        """

        # assign responses to each request sent to a specific url
        dashboard = self.app.test_client().get('/dashboard')
        create_shopping_list = self.app.test_client().\
            get('create-shopping-list')
        shopping_list_detail = self.app.test_client().\
            get('/shopping-list-detail/?name=birthday')
        remove_shopping_list = self.app.test_client().\
            get('/remove-shopping-list?name=birthday')
        remove_shopping_item = self.app.test_client().\
            get('/remove-shopping-item?name=birthday-item')
        update_shopping_list = self.app.test_client().\
            get('/update-item?name=birthday-item')
        update_shopping_item = self.app.test_client().\
            get('/update-shopping-list?name=birthday-item')

        # Dashboard view
        self.assertIn(b'Redirecting...', dashboard.data)
        self.assertTrue(dashboard.status_code == 302)

        # CreateShoppingList view
        self.assertIn(b'Redirecting...', create_shopping_list.data)
        self.assertTrue(create_shopping_list.status_code == 302)

        # ShoppingListDetail view
        self.assertIn(b'Redirecting...', shopping_list_detail.data)
        self.assertTrue(shopping_list_detail.status_code == 302)

        # RemoveShoppingList view
        self.assertIn(b'Redirecting...', remove_shopping_list.data)
        self.assertTrue(remove_shopping_list.status_code == 302)

        # RemoveShoppingItem view
        self.assertIn(b'Redirecting...', remove_shopping_item.data)
        self.assertTrue(remove_shopping_item.status_code == 302)

        # UpdateShoppingList view
        self.assertIn(b'Redirecting...', update_shopping_list.data)
        self.assertTrue(update_shopping_list.status_code == 302)

        # UpdateShoppingItem view
        self.assertIn(b'Redirecting...', update_shopping_item.data)
        self.assertTrue(update_shopping_item.status_code == 302)
