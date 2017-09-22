import datetime

from flask import flash, redirect, render_template, request, session, url_for
from flask.views import View
from .db.models import ShoppingList, ShoppingItem
from .utils.helpers import json_serial


class RegisterView(View):
    methods = ['GET', 'POST']

    def dispatch_request(self):
        if 'user' in session:
            flash('you are already logged in!')
            return redirect(url_for('index'))

        if request.method == 'POST':
            # get required data
            username = request.form.get('username')
            password1 = request.form.get('password1')
            password2 = request.form.get('password2')

            # validate password match
            if password1 == password2:
                session['user'] = username  # add user to session

                flash('Success! you are now a member')
                return redirect(url_for('index'))  # redirect to index

            flash('Error!! passwords do not match')
            redirect(url_for('register'))

        return render_template('register.html')


class LoginView(View):
    """Class that handles user login"""
    methods = ['GET', 'POST']

    def dispatch_request(self):
        if 'user' in session:
            flash('you are already logged in!')
            return redirect(url_for('index'))

        if request.method == 'POST':
            username = request.form.get('username')

            session['user'] = username
            flash('You are logged in')
            return redirect(url_for('index'))

        return render_template('login.html')


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

        return render_template('index.html', is_auth=is_auth)


class DashboardView(View):
    methods = ['GET', ]

    def dispatch_request(self):
        is_auth = False

        if 'user' not in session:  # check if user is logged in
            flash('you must be logged in, or create an account if you dont have one')
            return redirect(url_for('login'))

        if 'user' in session:
            is_auth = True

        user = session.get('user')

        return render_template('dashboard.html', is_auth=is_auth)


class CreateShoppingList(View):
    """Class to create shopping list"""

    methods = ['GET', 'POST']

    def dispatch_request(self):
        is_auth = False

        if 'user' not in session:  # check if user is logged in
            flash('you must be logged in, or create an account if you dont have one')
            return redirect(url_for('login'))

        if 'user' in session:
            is_auth = True

        if request.method == 'POST':
            name = request.form.get('name')

        return render_template('shopping_list/create_shopping_list.html', is_auth=is_auth)


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
    methods = ['POST', ]

    def dispatch_request(self):
        user = session.get('user')
        name = request.args.get('name')
        rm = ShoppingList().delete_shopping_list(user, name)
        if rm:
            flash('Shopping list deleted')
            return redirect(url_for('dashboard'))

        flash('try again')
        return redirect(url_for('remove-shopping-list', name=name))
