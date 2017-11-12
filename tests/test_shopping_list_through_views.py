"""Tests ShoppingList and ShoppingItem through views"""

import unittest
from .base import ShoppingListTestBase


class TestShoppingListThroughViews(ShoppingListTestBase):
    """
        Test class to test Shopping List and Shopping Items CRUD
        operations through views
    """
    def setUp(self):
        super(TestShoppingListThroughViews, self).setUp()
        client = self.app.test_client()
        user_cridentials = {'username': 'gideon',
                            'password': 'gideonpassword'}
        client.post('/register', data=dict(username=user_cridentials.get('username'),
                                           email='gideon@gmail.com',
                                           password=user_cridentials.get('password'),
                                           confirm=user_cridentials.get('password')),
                    follow_redirects=True)  # register client
        self.client = client
        self.user_cridentials = user_cridentials  # cridentials to authenticate user.

    def test_create_shoppinglist(self):
        """
        User can create shoppinglist object.
        """

        name = 'Birthday'  # name of the shopping list
        with self.client as client:
            #  login user
            client.post('/login',
                        data=dict(username=self.user_cridentials.get('username'),
                                  password=self.user_cridentials.get('password')))

            # create shopping list
            create_resp = client.post('/create-shopping-list', data=dict(name=name),
                                      follow_redirects=True)

            # assertions.
            self.assert200(create_resp)
            self.assertIn(name, create_resp.get_data(as_text=True))

    def test_retrieve_shoppinglist(self):
        """
        User can retrieve created shoppinglist object.
        """

        name = 'Birthday'  # name of the shopping list
        with self.client as client:
            #  login user
            client.post('/login',
                        data=dict(username=self.user_cridentials.get('username'),
                                  password=self.user_cridentials.get('password')))

            # create shoppinglist object.
            client.post('/create-shopping-list', data=dict(name=name),
                        follow_redirects=True)

            # retrieve shoppinglist object.
            view_resp = client.get('/shopping-list-detail/?name=%(name)s'
                                   % dict(name=name))

            # assertions.
            self.assert200(view_resp)  # 200 if request is successful.
            self.assertIn(name, view_resp.get_data(as_text=True))

    def test_update_shoppinglist(self):
        """
        User should update created shoppinglist.
        """

        name = 'Birthday'  # name of the shopping list
        with self.client as client:
            #  login user
            client.post('/login',
                        data=dict(username=self.user_cridentials.get('username'),
                                  password=self.user_cridentials.get('password')))

            # create shoppinglist object.
            client.post('/create-shopping-list', data=dict(name=name),
                        follow_redirects=True)

            # update shoppinglist object.
            new_name = 'Birthday Party'
            update_resp = client.post('/update-shopping-list/?name=%(name)s' % dict(name=name),
                                      data=dict(name=new_name), follow_redirects=True)

            self.assert200(update_resp)
            self.assertIn(new_name, update_resp.get_data(as_text=True))
            self.assertMessageFlashed('Shopping list name changed successfully', 'success')

    def test_delete_shoppinglist(self):
        """
        User should delete created shoppinglist.
        """

        name = 'Birthday'  # name of the shopping list
        with self.client as client:
            #  login user
            client.post('/login',
                        data=dict(username=self.user_cridentials.get('username'),
                                  password=self.user_cridentials.get('password')))

            # create shoppinglist object.
            client.post('/create-shopping-list', data=dict(name=name),
                        follow_redirects=True)

            # remove shopping list
            delete_resp = client.get('/remove-shopping-list/?name=%(name)s'
                                     % dict(name=name),
                                     follow_redirects=True)  # remove shopping list detail

            self.assertMessageFlashed('Success!! Shopping List removed', 'success')
            self.assert200(delete_resp)

    def test_create_shoppingitem(self):
        """
        Client should add shoppingitem object to shoppinglist object.
        """

        shoppinglist_name = 'Birthday'  # name of the shopping list.
        shoppingitem_one = dict(item_name='Cup cake',
                                quantity='10',
                                price='100')  # shopping item one data.
        shoppingitem_two = dict(item_name='Juice',
                                quantity=2,
                                price=200)  # shopping item two data.

        with self.client as client:

            # login user
            login_resp = client.post('/login',
                                     data=dict(username=self.user_cridentials.get('username'),
                                               password=self.user_cridentials.get('password')))

            self.assertRedirects(login_resp, '/')  # assert if user is redirected to index page

            # create shopping list
            client.post('/create-shopping-list',
                        data=dict(name=shoppinglist_name),
                        follow_redirects=True)

            # create shoppingitems.
            resp_one = client.post('/shopping-list-detail/?name=%(name)s' %
                                   dict(name=shoppinglist_name), data=shoppingitem_one,
                                   follow_redirects=True)

            resp_two = client.post('/shopping-list-detail/?name=%(name)s' %
                                   dict(name=shoppinglist_name), data=shoppingitem_two,
                                   follow_redirects=True)

            # assertions.
            self.assert200(resp_one)
            self.assert200(resp_two)
            self.assertMessageFlashed('Item successfully added', 'success')

    def test_retrieve_shoppingitem(self):
        """
        User should retrieve created shoppingitem object.
        """

        shoppinglist_name = 'Birthday'  # name of the shopping list.
        shoppingitem_one = dict(item_name='Cup cake',
                                quantity='10',
                                price='100')  # shopping item one data.
        shoppingitem_two = dict(item_name='Juice',
                                quantity=2,
                                price=200)  # shopping item two data.

        with self.client as client:
            # login user
            login_resp = client.post('/login',
                                     data=dict(username=self.user_cridentials.get('username'),
                                               password=self.user_cridentials.get('password')))

            self.assertRedirects(login_resp, '/')  # assert if user is redirected to index page

            # create shopping list
            client.post('/create-shopping-list',
                        data=dict(name=shoppinglist_name),
                        follow_redirects=True)

            # create shoppingitems.
            client.post('/shopping-list-detail/?name=%(name)s' %
                        dict(name=shoppinglist_name), data=shoppingitem_one,
                        follow_redirects=True)

            client.post('/shopping-list-detail/?name=%(name)s' %
                        dict(name=shoppinglist_name), data=shoppingitem_two,
                        follow_redirects=True)

            # retrieve shoppinglist object.
            view_resp = client.get('/shopping-list-detail/?name=%(name)s' %
                                   dict(name=shoppinglist_name))

            self.assert200(view_resp)
            self.assertIn(shoppingitem_one.get('item_name'),
                          view_resp.get_data(as_text=True))
            self.assertIn(shoppingitem_two.get('item_name'),
                          view_resp.get_data(as_text=True))

    def test_update_shoppingitem(self):
        """
        User should update shoppingitem object.
        """

        shoppinglist_name = 'Birthday'  # name of the shopping list.
        shoppingitem = dict(item_name='Cup cake',
                            quantity='10',
                            price='100')  # shopping item one data.

        with self.client as client:

            # login user
            login_resp = client.post('/login',
                                     data=dict(username=self.user_cridentials.get('username'),
                                               password=self.user_cridentials.get('password')))

            self.assertRedirects(login_resp, '/')  # assert if user is redirected to index page

            # create shopping list
            client.post('/create-shopping-list',
                        data=dict(name=shoppinglist_name),
                        follow_redirects=True)

            # create shoppingitems.
            client.post('/shopping-list-detail/?name=%(name)s' %
                        dict(name=shoppinglist_name), data=shoppingitem,
                        follow_redirects=True)

            # update shoppingitem.
            new_item_name = 'Chicken wings'

            update_shopping_item_resp = \
                client.post('/update-item/?sname=%(sname)s&iname=%(iname)s' %
                            dict(sname=shoppinglist_name,
                                 iname=shoppingitem.get('item_name')),
                            data=dict(item_name=new_item_name,
                                      quantity=shoppingitem.get('quantity'),
                                      price=shoppingitem.get('price')),
                            follow_redirects=True)

            self.assertMessageFlashed('Item successfully updated', 'success')
            self.assertIn(new_item_name, update_shopping_item_resp.get_data(as_text=True))

    def test_delete_shoppingitem(self):
        """
        User should delete shoppingitem object.
        """

        shoppinglist_name = 'Birthday'  # name of the shopping list.
        shoppingitem = dict(item_name='Cup cake',
                            quantity='10',
                            price='100')  # shopping item one data.

        with self.client as client:

            # login user
            login_resp = client.post('/login',
                                     data=dict(username=self.user_cridentials.get('username'),
                                               password=self.user_cridentials.get('password')))

            self.assertRedirects(login_resp, '/')  # assert if user is redirected to index page

            # create shopping list
            client.post('/create-shopping-list',
                        data=dict(name=shoppinglist_name),
                        follow_redirects=True)

            # create shoppingitems.
            client.post('/shopping-list-detail/?name=%(name)s' %
                        dict(name=shoppinglist_name), data=shoppingitem,
                        follow_redirects=True)

            # delete shoppingitem.
            del_response = \
                client.get('/remove-shopping-item/?name=%(sname)s&item_name=%(iname)s' %
                           dict(sname=shoppinglist_name, iname=shoppingitem.get('item_name')),
                           follow_redirects=True)

            self.assert200(del_response)
            self.assertMessageFlashed('Success!! Item succesfully removed', 'success')

    def test_non_existence(self):
        """
        tests for non existing shoppinglists and shoppingitems with authenticated user.
        """

        with self.client as client:
            # attempt to delete a shopping list
            del_response = client.get('/remove-shopping-item/?name=HomeComings&item_name=Pizza',
                                      follow_redirects=True)

            self.assertMessageFlashed('you must be logged in, '
                                      'or create an account if you dont have one')

            # login user
            client.post('/login', data=dict(username=self.user_cridentials.get('username'),
                                            password=self.user_cridentials.get('password')))

            # try and access random shopping list name
            response_one = client.get('/shopping-list-detail/?name=Random+List')
            response_two = client.get('/shopping-list-detail/?name=Random+List',
                                      follow_redirects=True)

            # test for redirection
            self.assertRedirects(response_one, '/dashboard')

            # test for error message
            self.assertMessageFlashed('The requested shopping list does not exist!', 'danger')
