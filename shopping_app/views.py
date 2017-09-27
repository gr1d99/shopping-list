import datetime

import main
from flask import flash, redirect, render_template, request, session, url_for
from flask.views import View
from .db.models import ShoppingList, ShoppingItem, ShoppingListManager, User
from .forms import LoginForm, CreateShoppingItemForm
from .utils.helpers import json_serial, check_name, get_shl, check_duplicate_item_name


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

        return render_template(
            'register.html', title='Register'
        )


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

        return render_template('login.html',
                               form=form,
                               title='Login')


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
        print(session)

        is_auth = False
        if 'user' in session:
            is_auth = True
        return render_template('index.html',
                               is_auth=is_auth,
                               title='Home Page')


class DashboardView(View):
    methods = ['GET', ]

    def dispatch_request(self):
        is_auth = False

        user_shopping_list = main.app.shopping_list

        if 'user' not in session:  # check if user is logged in
            flash('you must be logged in, or create an account if you dont have one')
            return redirect(url_for('login'))

        if 'user' in session:
            is_auth = True

        shopping_lists = [ushl for ushl in user_shopping_list]

        return render_template('dashboard.html',
                               is_auth=is_auth,
                               shopping_lists=shopping_lists,
                               title='Dashboard')


class CreateShoppingList(View):
    methods = ['GET', 'POST']

    def dispatch_request(self):
        is_auth = False

        if 'user' not in session:
            flash(u'Warning!! you must be logged in', 'warning')
            return redirect(url_for('login'))

        if 'user' in session:
            is_auth = True

        if request.method == 'POST':
            name = request.form.get('shl-name')

            # check if shopping list name exists
            for shl in main.app.shopping_list:
                if shl.get('name') == name:
                    flash(u'Shopping list with that name already exists, try another name', 'warning')
                    return redirect(url_for('create-shopping-list'))
            try:
                user = main.app.user.get_user(
                    session.get('user')
                )

            except Exception:
                main.app.user.create_user(session.get('user'), session.get('user'), '')
                user = main.app.user.get_user(
                    session.get('user')
                )
            check_name(name)
            today = datetime.datetime.now().strftime("%Y-%m-%w")
            shl = ShoppingList()
            shl.create(name, user, today)
            main.app.shopping_list.append({'name': name, 'shl': shl})

            flash(u'Shopping list created', 'success')
            return redirect(url_for('dashboard'))

        return render_template(
            'shopping_list/create-shopping-list.html',
            is_auth=is_auth, title='Create Shopping List')


class NewShoppingListDetailView(View):
    methods = ['GET', 'POST']

    def dispatch_request(self):
        is_auth = False

        if 'user' not in session:  # check if user is logged in
            flash('you must be logged in, or create an account if you dont have one')
            return redirect(url_for('login'))

        if 'user' in session:
            is_auth = True

        form = CreateShoppingItemForm()
        shl = None
        name = request.args.get('name')
        if check_name(name):
            shl = get_shl(name)

        if request.method == 'POST':
            form = CreateShoppingItemForm(request.form)
            if not form.validate():
                flash(u'Please correct the errors below', 'warning')

            else:
                shl_item = main.app.shopping_item()
                item_name = form.item_name.data

                if check_duplicate_item_name(name, item_name):
                    flash(u"item with that name already exists", 'warning')

                else:
                    item_quantity = form.quantity.data
                    item_price = form.price.data
                    shl_item.create(item_name, int(item_quantity), float(item_price), False)
                    shl.get('shl').items.append(shl_item)
                    flash(u'Item successfully added', 'success')
                    return redirect(url_for('shopping-list-detail', name=name))

        return render_template(
            'shopping_list/shopping_list_detail.html',
            obj=shl, form=form, is_auth=is_auth)


class UpdateItemView(View):
    """
    A view to update each individual item
    """
    methods = ['GET', 'POST']

    def dispatch_request(self):
        shopping_list_name = request.args.get('shl_name')
        item_name = request.args.get('item_name')

        print(check_name(shopping_list_name))

        return redirect(url_for('shopping-list-detail', name=shopping_list_name))


class MarkItemView(View):
    """
    A view to check and uncheck items in a view
    """

    methods = ['GET', 'POST',]

    def dispatch_request(self):
        if request.method == 'POST':
            shl_name, item_name, prev_val = request.form.get('shl-name'), \
                                            request.form.get('item-name'), \
                                            request.form.get('prev-val')

            shl = get_shl(shl_name).get('shl')
            for shl_item in shl.items:
                if prev_val == 'False':
                    shl_item.update('checked', True)
                else:
                    shl_item.update('checked', False)
            flash(u'Success!! item updated', 'success')
            return redirect(url_for('shopping-list-detail', name=shl_name))
        return redirect(url_for('dashboard'))


class UpdateShoppingItemView(View):
    """A View to only update a single shopping item"""
    methods = ['GET', 'POST']

    def dispatch_request(self):
        if request.method == 'POST':
            shopping_list_name = request.form.get('shl-name')
            item_name = request.form.get('shl-name')


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
        return render_template('index.html')


class UpdateShoppingListItem(View):
    methods = ['GET', 'POST']

    def dispatch_request(self):
        flash('not yet implemented')
        return render_template('index.html')


class RemoveShoppingList(View):
    """A view to remove a single shopping list"""
    methods = ['GET', ]

    def dispatch_request(self):
        name = request.args.get('name')
        shl = get_shl(name)
        main.app.shopping_list.remove(shl)
        flash(u'Success!! Shopping List removed', 'success')
        return redirect(url_for('dashboard'))


class RemoveShoppingItem(View):
    """A view to remove shopping item"""
    methods = ['GET', 'POST']

    def dispatch_request(self):
        name = request.args.get('name')
        item_name = request.args.get('item_name')
        shl_items = get_shl(name).get('shl').items
        for item in shl_items:
            if item.name == item_name:
                shl_items.remove(item)
                flash(u"Success!! Item succesfully removed", 'success')

        return redirect(url_for('shopping-list-detail', name=name))