"""
This module contains User and Views authentication tests
"""

from .test_base import ShoppingListTestBase


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
        self.assertIn(b'Success! you may now login using your username and password', resp.data)

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
        self.assertIn(b'you must be logged in, or create an account if you dont have one',
                      self.client.get('/dashboard', follow_redirects=True).data)

    def test_duplicate_username(self):
        """
            test if it will throw an error if username is reused
        """
        resp = self.client.post('/register', data=dict(username='gideon',
                                                       email='gideon@gmail.com',
                                                       password='password12',
                                                       confirm='password12'),
                                follow_redirects=True)
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
        self.assertIn(bytes(error_message.encode('ascii')),  resp.data)

    def test_after_login(self):
        """
        Test if user can still access registration and login views
        :return:
        """
        with self.client as client:
            client.post('/login',
                        data=dict(username='gideon', password='password12'),
                        follow_redirects=True)

            reg_resp = client.get('/register', follow_redirects=True)
            login_resp = client.get('/login', follow_redirects=True)

            self.assertIn(b'you are already logged in!', reg_resp.data, login_resp.data)
