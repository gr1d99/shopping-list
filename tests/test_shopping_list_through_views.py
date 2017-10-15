"""Tests ShoppingList and ShoppingItem through views"""

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
        self.user_cridentials = user_cridentials  # cridentials to authenticate user

    def test_shopping_list_crud(self):
        """
            test if user can create and view shopping list
        """
        name = 'Birthday'  # name of the shopping list
        with self.client as client:

            #  login user
            login_resp = client.post('/login',
                                     data=dict(username=self.user_cridentials.get('username'),
                                               password=self.user_cridentials.get('password')))

            self.assertRedirects(login_resp, '/')  # assert if user is redirected to index page

            # create shopping list
            create_resp = client.post('/create-shopping-list', data=dict(name=name),
                                      follow_redirects=True)

            self.assert200(create_resp)
            self.assertIn(bytes(name.encode('ascii')), create_resp.data)

            # view shopping list
            view_resp = client.get('/shopping-list-detail/?name=%(name)s'
                                   % dict(name=name))  # get shopping list detail

            self.assert200(view_resp)
            self.assertIn(bytes(name.encode('ascii')), view_resp.data)

            # update shopping list
            new_name = 'Birthday Party'
            update_resp = client.post('/update-shopping-list/?name=%(name)s' % dict(name=name),
                                      data=dict(name=new_name), follow_redirects=True)

            self.assert200(update_resp)
            self.assertIn(bytes(new_name.encode('ascii')), update_resp.data)
            self.assertMessageFlashed('Shopping list name changed successfully', 'success')

            # remove shopping list
            delete_resp = client.get('/remove-shopping-list/?name=%(name)s'
                                     % dict(name=new_name),
                                     follow_redirects=True)  # remove shopping list detail
            # using updated new name

            self.assertMessageFlashed('Success!! Shopping List removed', 'success')
            self.assert200(delete_resp)

    def test_create_shopping_item(self):
        """
            test if shopping item is added to the shopping list
        """

        shopping_list_name = 'Birthday'  # name of the shopping list
        shopping_item_one = dict(item_name='Cup cake',
                                 quantity='10',
                                 price='100')  # shopping item one data
        shopping_item_two = dict(item_name='Juice',
                                 quantity=2,
                                 price=200)  # shopping item two data

        with self.client as client:

            #  login user
            login_resp = client.post('/login',
                                     data=dict(username=self.user_cridentials.get('username'),
                                               password=self.user_cridentials.get('password')))

            self.assertRedirects(login_resp, '/')  # assert if user is redirected to index page

            # create shopping list
            create_shopping_list_resp = client.post('/create-shopping-list',
                                                    data=dict(name=shopping_list_name),
                                                    follow_redirects=True)

            self.assert200(create_shopping_list_resp)
            self.assertIn(bytes(shopping_list_name.encode('ascii')),
                          create_shopping_list_resp.data)
            self.assertMessageFlashed('Shopping list created', 'success')

            # create shopping item
            client.post('/shopping-list-detail/?name=%(name)s' %
                        dict(name=shopping_list_name), data=shopping_item_one,
                        follow_redirects=True)
            client.post('/shopping-list-detail/?name=%(name)s' %
                        dict(name=shopping_list_name), data=shopping_item_two,
                        follow_redirects=True)

            view_shopping_list_resp = client.get('/shopping-list-detail/?name=%(name)s'
                                                 % dict(name=shopping_list_name))
            self.assertIn(bytes(shopping_item_one.
                                get('item_name').encode('ascii')),
                          view_shopping_list_resp.data)
            self.assertIn(bytes(shopping_item_two.
                                get('item_name').encode('ascii')),
                          view_shopping_list_resp.data)
            self.assertMessageFlashed('Item successfully added', 'success')

            # update shopping item
            # update `shopping item one` name
            new_item_name = 'Chicken wings'

            update_shopping_item_resp = \
                client.post('/update-item/?sname=%(sname)s&iname=%(iname)s' %
                            dict(sname=shopping_list_name,
                                 iname=shopping_item_one.get('item_name')),
                            data=dict(item_name=new_item_name,
                                      quantity=shopping_item_one.get('quantity'),
                                      price=shopping_item_one.get('price')),
                            follow_redirects=True)

            self.assertMessageFlashed('Item successfully updated', 'success')
            self.assertIn(bytes(new_item_name.encode('ascii')), update_shopping_item_resp.data)

            # delete shopping item
            # delete `shopping_item_two`
            del_response = \
                client.get('/remove-shopping-item/?name=%(sname)s&item_name=%(iname)s' %
                           dict(sname=shopping_list_name, iname=shopping_item_two.get('item_name')),
                           follow_redirects=True)

            self.assertMessageFlashed('Success!! Item succesfully removed', 'success')
            self.assertTrue(bytes(shopping_item_two.get('item_name').encode('ascii'))
                            not in del_response.data)

    def test_non_existence(self):
        """
            tests for non existence shopping lists and shopping items with authenticated user
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
