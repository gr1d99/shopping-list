import datetime

from flask import flash, redirect, render_template, request, session, url_for
from flask.views import View
from .db.models import ShoppingList, User
from .utils.helpers import json_serial


class LoginView(View):
    """Class that handles user login"""
    methods = ['GET', 'POST']

    def dispatch_request(self):
        if 'user' in session:
            flash('you are already logged in!')
            return redirect(url_for('index'))

        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            auth = User()

            if not auth.authenticate(username, password):
                flash('Username and password do not match, try again!')
                return redirect(url_for('login'))

            session['user'] = username
            flash('You are logged in')
            return redirect(url_for('index'))

        return render_template('login.html')


class IndexView(View):
    """User home page view"""

    methods = ['GET', ]

    def dispatch_request(self):
        all_shopping_lists = ShoppingList().all()
        return render_template('index.html', shls=all_shopping_lists)


class DashboardView(View):
    methods = ['GET', ]

    def dispatch_request(self):
        if 'user' not in session:
            flash('you must be logged in, or create an account if you dont have one')
            return redirect(url_for('login'))

        user = session.get('user')
        shopping_list = ShoppingList().filter_user_shopping_list(user)

        return render_template('dashboard.html', shopping_list=shopping_list)


class RegisterView(View):
    methods = ['GET', 'POST']

    def dispatch_request(self):
        if 'user' in session:
            flash('you are already logged in!')
            return redirect(url_for('index'))

        if request.method == 'POST':
            username = request.form.get('username')
            password1 = request.form.get('password1')
            password2 = request.form.get('password2')

            if password1 == password2:  # validate passwords
                u = User()
                if not u.check_user(username):
                    u.create_user(username, password1)
                    session['user'] = username  # add user to session
                    flash('Successfully registered')
                    redirect(url_for('index'))  # redirect to homepage

                flash('user with that username already exists, try another name')
                return redirect(url_for('register'))

            flash('passwords do not match')
            return redirect(url_for('register'))

        return render_template('register.html')


class Logout(View):
    methods = ['GET', ]

    def dispatch_request(self):
        if 'user' in session:
            session.pop('user')
            flash('successfully logged out!')
            return redirect(url_for('index'))

        return redirect(url_for('index'))


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
