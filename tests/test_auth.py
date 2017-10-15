"""
This module contains User and Views authentication tests
"""

from .base import ShoppingListTestBase


class TestUserAuth(ShoppingListTestBase):
    """
        Test case that covers user registration, login, logout.
        it also tests if usernames and emails are already used.
    """

    def setUp(self):
        super(TestUserAuth, self).setUp()
        client = self.app.test_client()
        client.post('/register', data=dict(username='gideon',
                                           email='gideon@gmail.com',
                                           password='password12',
                                           confirm='password12'),
                    follow_redirects=True)
        self.client = client

    def test_user_registration(self):
        """
        Test if user is registered successfully
        """
        client = self.app.test_client()
        resp = client.post('/register', data=dict(username='emma',
                                                  email='emma@gmail.com',
                                                  password='emmapassword',
                                                  confirm='emmapassword'),
                           follow_redirects=True)  # create a new user by triggering post method
        self.assertMessageFlashed('Success! you may now login using your username and password', 'success')

    def test_user_login(self):
        """
        tests if user logins successfully after registering
        """
        # we will use the cridentials used to register new user
        # in setUp method
        resp = self.client.post('/login',
                                data=dict(username='gideon', password='password12'))

        self.assertRedirects(resp, '/')

    def test_user_logout(self):
        """
            tests if user is successfully logged out
        """
        resp = self.client.get('/logout')

        self.assertRedirects(resp, '/')
        # lets just check if the same user can access the dashboard after login
        dashboard_resp = self.client.get('/dashboard')
        self.assertMessageFlashed('you must be logged in, or create an account if you dont have one', 'warning')
        self.assertRedirects(dashboard_resp, '/login')  # user redirected to login page

    def test_duplicate_username(self):
        """
            test if it will throw an error if username is reused
        """
        resp = self.client.post('/register', data=dict(username='gideon',
                                                       email='gideon@gmail.com',
                                                       password='password12',
                                                       confirm='password12'))
        self.assertIn(b'gideon already taken', resp.data)

    def test_duplicate_email(self):
        """
            test if an error will be thrown if the same email is reused by
            another user
        """
        client = self.app.test_client()
        duplicate_email = 'gideon@gmail.com'  # use the same email as the
        # one used in setUp method
        resp = client.post('/register', data=dict(username='giddy',
                                                  email=duplicate_email,
                                                  password='password12',
                                                  confirm='password12'),
                           follow_redirects=True)

        error_message = '%(email)s already taken' % dict(email=duplicate_email)
        self.assertIn(bytes(error_message.encode('ascii')), resp.data)

    def test_after_login(self):
        """
        Test if user can still access registration and login views
        :return:
        """
        with self.client as client:
            client.post('/login',
                        data=dict(username='gideon', password='password12'),
                        follow_redirects=True)

            reg_response = client.get('/register')
            login_response = client.get('/login')

            self.assertMessageFlashed('you are already logged in!', 'info')
            self.assertRedirects(reg_response, '/')
            self.assertRedirects(login_response, '/')
