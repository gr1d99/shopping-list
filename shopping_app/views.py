import datetime

import main
from flask import flash, redirect, render_template, request, session, url_for
from flask.views import View
from .db.models import ShoppingList, ShoppingItem, ShoppingListManager, User
from .forms import LoginForm, RegistrationForm
from .utils.helpers import json_serial


class RegisterView(View):
    """A view class to handle """
    methods = ['GET', 'POST']

    def dispatch_request(self):

        if 'user' in session:
            flash(u'you are already logged in!', 'info')
            return redirect(url_for('index'))

        if request.method == 'POST':
            # get required data
            username = request.form.get('username')
            email = request.form.get('email')
            password1 = request.form.get('password1')
            password2 = request.form.get('password2')

            if not (username or password1 or password2):
                flash(u'Hey!! do not submit empty data', 'warning')
                return redirect(url_for('register'))

            # validate password match
            if password1 == password2:
                main.app.user.create_user(username, password1, email)

                session['user'] = username  # add user to session

                flash(u'Success! you are now a member', 'success')
                return redirect(url_for('index'))  # redirect to index

            flash(u'Error!! passwords do not match', 'warning')
            redirect(url_for('register'))

        return render_template('register.html')


class LoginView(View):
    """Class that handles user login"""
    methods = ['GET', 'POST']

    def dispatch_request(self):
        form = LoginForm(request.form)
        if 'user' in session:
            flash(u'you are already logged in!', 'info')
            return redirect(url_for('index'))

        if request.method == 'POST':
            if not form.validate():
                flash(u'Please check the errors below', 'warning')

            username = form.username.data
            password = form.password.data

            if not main.app.user.validate_user(username, password):
                flash('username or password is incorrect', 'warning')
                return redirect(url_for('login'))

            flash(u'Success!! you are now logged in', 'success')
            session['user'] = username

            return redirect(url_for('index'))

        return render_template('login.html', form=form)


class Logout(View):
    methods = ['GET', ]

    def dispatch_request(self):
        if 'user' in session:
            session.pop('user')
            flash('successfully logged out!')
            return redirect(url_for('index'))

        return redirect(url_for('index'))


class IndexView(View):
    """User home page view"""

    methods = ['GET', ]

    def dispatch_request(self):

        is_auth = False
        if 'user' in session:
            is_auth = True

        shopping_list = []
        if 'shopping_list' in session:
            shopping_list = session.get('shopping_list')

        return render_template('index.html', is_auth=is_auth, shopping_list=shopping_list)


class DashboardView(View):
    methods = ['GET', ]

    def dispatch_request(self):
        is_auth = False

        shopping_list = []

        if 'shopping_list' in session:
            shopping_list = session.get('shopping_list')

        if 'user' not in session:  # check if user is logged in
            flash('you must be logged in, or create an account if you dont have one')
            return redirect(url_for('login'))

        if 'user' in session:
            is_auth = True

        shopping_lists = [ushl.name for ushl in user_shopping_list]

        return render_template('dashboard.html', is_auth=is_auth, shopping_lists=shopping_lists)


class CreateShoppingList(View):
    methods = ['GET', 'POST']

    def dispatch_request(self):
        is_auth = False

        if 'user' in session:
            is_auth = True

        if request.method == 'POST':
            print(user.users)

            name = request.form.get('shl-name')
            logged_in_user = session.get('user')

            try:  # force creation of user
                user.get_user(logged_in_user)

            except Exception:
                user.create_user(logged_in_user, logged_in_user, '')

            ShoppingList().create(name, user.get_user(session.get('user')),
                       datetime.datetime.today().strftime("%Y-%m-%w"))

            user_shopping_list.append(shl)

            flash('Shopping list created')
            return redirect(url_for('dashboard'))

        return render_template(
            'shopping_list/create-shopping-list.html',
            is_auth=is_auth)

# class CreateShoppingList(View):
#     """Class to create shopping list and items"""
#
#     methods = ['GET', 'POST']
#
#     def dispatch_request(self):
#         is_auth = False
#
#         if 'user' not in session:  # check if user is logged in
#             flash('you must be logged in, or create an account if you dont have one')
#             return redirect(url_for('login'))
#
#         if 'user' in session:
#             is_auth = True
#
#         if request.method == 'POST':
#             # TODO Add WTForms
#             name = request.form.get('shl-name')  # shopping list name
#
#             item1_name = request.form.get('item_1_name')
#             item1_price = request.form.get('item_1_price')
#             item1_check = bool(request.form.get('item_1_check') == 'on')
#
#             item2_name = request.form.get('item_2_name')
#             item2_price = request.form.get('item_2_price')
#             item2_check = bool(request.form.get('item_2_check') == 'on')
#
#             item3_name = request.form.get('item_3_name')
#             item3_price = request.form.get('item_3_price')
#             item3_check = bool(request.form.get('item_3_check') == 'on')
#
#             today = datetime.datetime.today().strftime('%Y-%m-%w')
#
#             # create shopping items first
#             shoppingitem1 = ShoppingItem(item1_name, item1_price, item1_check)
#             shoppingitem2 = ShoppingItem(item2_name, item2_price, item2_check)
#             shoppingitem3 = ShoppingItem(item3_name, item3_price, item3_check)
#
#             # create a shopping list
#             shoppinglist = ShoppingList(name, date_added=today)
#             shoppinglist.add(shoppingitem1, shoppingitem2, shoppingitem3)
#
#             # add stored data into the session
#             if 'shopping_list' not in session:  # TODO lear more on serialization of objects
#                 session['shopping_list'] = [shoppinglist.__dict__]
#
#             prev_data = session.get('shopping_list')
#             prev_data.append(shoppinglist.__dict__)
#             session['shopping_list'] = prev_data
#
#             return redirect(url_for('dashboard'))
#
#         return render_template(
#             'shopping_list/create_shopping_list.html',
#             is_auth=is_auth)


class AddItemsView(View):
    methods = ['GET', 'POST']

    def dispatch_request(self):
        if request.method == 'POST':
            shopping_list_name = request.form.get('name')
            category = request.form.get('category')
            item_names = ['item1', 'item2', 'item3']
            items = [request.form.get(item) for item in item_names]

            # Add Items posted by the user to the ShoppingList model
            # create an instace
            s = ShoppingList()
            s.create_shopping_list(session['user'],
                                   shopping_list_name,
                                   category,
                                   json_serial(datetime.date.today()),
                                   items)
            if True:
                flash('Shopping list successfully created')
                return redirect(url_for('dashboard'))
        return render_template('shopping_list/create_shopping_list.html')


class ShoppingListDetail(View):
    methods = ['GET', ]

    def dispatch_request(self):
        name = request.args.get('name')  # name of the shopping list the user wants
        user = session['user']
        obj = ShoppingList().filter_user_shopping_list(user, name)[0]
        return render_template('shopping_list/shopping_list_detail.html', obj=obj, name=name)


class UpdateShoppingList(View):
    methods = ['GET', 'POST']

    def dispatch_request(self):
        flash('not yet implemented')
        return render_template('index.html')


class UpdateShoppingListItem(View):
    methods = ['GET', 'POST']

    def dispatch_request(self):
        flash('not yet implemented')
        return render_template('index.html')


class RemoveShoppingList(View):
    methods = ['GET', ]

    def dispatch_request(self):
        name = request.args.get('name')
        lists = session.get('shopping_list')
        index = 0
        target = None
        for l in lists:
            if l.get('name') == name:
                target = l
                break
            index += 1
        if target:
            lists.remove(target)
            session['shopping_list'] = lists
            flash('%s removed from shopping list')

        return redirect(url_for('dashboard'))
