"""This module contains all necessary views to power up shopping list web application"""

import time

import main
from flask import flash, redirect, render_template, request, session, url_for
from flask.views import View
from .db.shopping_list.shopping import ShoppingList
from .forms import (CreateShoppingItemForm, CreateShoppingListForm, LoginForm, RegistrationForm)
from .utils.helpers import (check_name, get_shl, check_duplicate_item_name,
                            change_shl_name, check_item, get_item, check_username,
                            check_email, get_user)


class RegisterView(View):

    """A view class to handle """

    methods = ['GET', 'POST']

    def dispatch_request(self):

        form = RegistrationForm(request.form)

        if 'user' in session:
            flash(u'you are already logged in!', 'info')
            return redirect(url_for('index'))

        if request.method == 'POST':
            # get required data
            form = RegistrationForm(request.form)
            if form.validate():
                username = form.username.data
                email = form.email.data
                password1 = form.password.data

                errors = []

                if not check_username(username):  # check username is already taken
                    if not check_email(email):  # check if email is taken
                        user = main.APP.user_manager.create_user(username, email, password1)
                        main.APP_USERS.insert(0, user)
                        flash(u'Success! you may now login using '
                              u'your username and password', 'success')
                        return redirect(url_for('index'))

                    else:
                        error = '%(email)s already taken' % dict(email=email)
                        errors.append(error)

                else:
                    error = '%(username)s already taken' % dict(username=username)
                    errors.append(error)

                flash(u'%(errors)s' % dict(errors=', '.join(errors)), 'warning')

        return render_template('register.html', title='Register', form=form)


class LoginView(View):

    """Class that handles user login"""

    methods = ['GET', 'POST']

    def dispatch_request(self):
        if 'user' in session:
            flash(u'you are already logged in!', 'info')
            return redirect(url_for('index'))

        form = LoginForm()
        if request.method == 'POST':
            form = LoginForm(request.form)
            if form.validate():
                username = form.username.data
                password = form.password.data
                user = get_user(username)
                if user is not False:
                    if user.verify_password(password):
                        session['user'] = username
                        flash(u'Success!! you are now logged in', 'success')
                        return redirect(url_for('index'))

                flash(u'incorrect username or password', 'info')

        return render_template('login.html', form=form, title='Login')


class LogoutView(View):

    """A view to logout a user"""

    methods = ['GET', ]

    def dispatch_request(self):
        if 'user' in session:
            session.pop('user')
            return redirect(url_for('index'))
        flash(u'successfully logged out!', 'success')
        return redirect(url_for('index'))


class IndexView(View):

    """User home page view"""

    methods = ['GET', ]

    def dispatch_request(self):
        is_auth = False
        if 'user' in session:
            is_auth = True
        return render_template('index.html', is_auth=is_auth, title='Home Page')


class DashboardView(View):

    """A view to display user dashboard"""

    methods = ['GET', ]

    def dispatch_request(self):
        is_auth = False
        username = None

        if 'user' not in session:  # check if user is logged in
            flash('you must be logged in, or create an account if you dont have one')
            return redirect(url_for('login'))

        if 'user' in session:
            is_auth = True
            username = session.get('user')

        owner = session.get('user')
        user_shopping_list = [ushl for ushl in main.APP.shopping_list
                              if owner == ushl.get('shl').added_by]

        return render_template('dashboard.html', is_auth=is_auth,
                               shopping_lists=user_shopping_list, title='Dashboard',
                               username=username)


class CreateShoppingListView(View):
    """A view to create shopping list"""
    methods = ['GET', 'POST']

    def dispatch_request(self):
        form = CreateShoppingListForm()
        is_auth = False

        if 'user' not in session:
            flash(u'Warning!! you must be logged in', 'warning')
            return redirect(url_for('login'))

        if 'user' in session:
            is_auth = True

        if request.method == 'POST':
            form = CreateShoppingListForm(request.form)
            if form.validate():
                name = form.name.data

                # check if shopping list name exists
                if not check_name(name):
                    user = session.get('user')
                    today = time.strftime("%x")
                    shl = ShoppingList()
                    shl.create(name, user, today)
                    main.APP.shopping_list.append({'name': name, 'shl': shl})
                    flash(u'Shopping list created', 'success')
                    return redirect(url_for('dashboard'))

                flash(u'Shopping list with that name already exists, '
                      u'try another name', 'warning')

            flash(u'Correct the errors', 'warning')

        return render_template('shopping_list/create-shopping-list.html', is_auth=is_auth,
                               title='Create Shopping List', form=form)


class ShoppingListDetailView(View):
    """
    A View to handle retrieval of a specific shopping list and creation of
    its shopping items
    """
    methods = ['GET', 'POST']

    def dispatch_request(self):
        is_auth = False

        if 'user' not in session:  # check if user is logged in
            flash('you must be logged in, or create an account if you dont have one')
            return redirect(url_for('login'))

        if 'user' in session:
            is_auth = True

        form = CreateShoppingItemForm()
        name = request.args.get('name')

        if not check_name(name):
            flash(u'The requested shopping list does not exist!', 'danger')
            return redirect(url_for('dashboard'))

        shl = get_shl(name)

        if request.method == 'POST':
            form = CreateShoppingItemForm(request.form)
            if form.validate():
                shl_item = main.APP.shopping_item()
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

                flash(u'Please correct the errors below', 'warning')

        return render_template(
            'shopping_list/shopping-list-detail.html',
            obj=shl, form=form, is_auth=is_auth, title=name.capitalize())


class UpdateShoppingListView(View):
    """
    A class to update shopping list
    """
    methods = ['GET', 'POST']

    def dispatch_request(self):
        name = request.args.get('name')
        form = CreateShoppingListForm(name=name)

        if not check_name(name):
            flash(u'The requested shopping list does not exist', 'danger')
            return redirect(url_for('dashboard'))

        if request.method == 'POST':
            form = CreateShoppingListForm(request.form)
            if form.validate():
                new_name = form.name.data
                shl = get_shl(name)
                shl.get('shl').update('name', new_name)
                change_shl_name(name, new_name)
                flash(u'Shopping list name changed successfully', 'success')
                return redirect(url_for('dashboard'))

        return render_template('shopping_list/shopping-list-edit.html', form=form, name=name)


class UpdateShoppingItemView(View):
    """
    A View to only update a single shopping item
    """
    methods = ['GET', 'POST']

    def dispatch_request(self):
        is_auth = False

        if 'user' not in session:  # check if user is logged in
            flash('you must be logged in, or create an account if you dont have one')
            return redirect(url_for('login'))

        if 'user' in session:
            is_auth = True

        name = request.args.get('sname')  # name of the shopping list
        item_name = request.args.get('iname')

        if not check_name(name):
            flash(u'The requested shopping list does not exist', 'warning')
            return redirect(url_for('dashboard'))

        if not check_item(name, item_name):
            flash(u'The requested shopping item does not exist', 'warning')
            return redirect(url_for('dashboard'))

        prev_data = {}

        for item in get_shl(name).get('shl').items:
            if item.name == item_name:
                prev_data.update({'name': item.name})
                prev_data.update({'quantity': item.quantity})
                prev_data.update({'price': item.price})
                prev_data.update({'checked': item.checked})
                break

        if not prev_data:
            flash(u'The shopping item you are trying to update does not exist', 'danger')

        form = CreateShoppingItemForm(
            item_name=prev_data.pop('name'),
            quantity=prev_data.pop('quantity'),
            price=prev_data.pop('price'),
            checked=prev_data.pop('checked')
        )

        if request.method == 'POST':
            form = CreateShoppingItemForm(request.form)
            if form.validate():
                new_item_name = form.item_name.data
                new_quantity = int(form.quantity.data)
                new_price = float(form.price.data)
                checked = form.checked.data

                item = get_item(name, item_name)
                if item:
                    item.update('name', new_item_name)
                    item.update('quantity', new_quantity)
                    item.update('price', new_price)
                    item.update('checked', checked)
                    flash(u'Item successfully updated', 'success')
                    return redirect(url_for('shopping-list-detail', name=name))

        return render_template('shopping_list/shopping-item-edit.html', form=form,
                               item_name=item_name, is_auth=is_auth,
                               title='Update %(item)s' % dict(item=item_name))


class RemoveShoppingListView(View):
    """A view to remove a single shopping list"""
    methods = ['GET', ]

    def dispatch_request(self):
        is_auth = False

        if 'user' not in session:  # check if user is logged in
            flash('you must be logged in, or create an account if you dont have one')
            return redirect(url_for('login'))

        if 'user' in session:
            is_auth = True

        name = request.args.get('name')
        shl = get_shl(name)
        main.APP.shopping_list.remove(shl)
        flash(u'Success!! Shopping List removed', 'success')
        return redirect(url_for('dashboard'))


class RemoveShoppingItemView(View):
    """A view to remove shopping item"""
    methods = ['GET', 'POST']

    def dispatch_request(self):

        is_auth = False

        if 'user' not in session:  # check if user is logged in
            flash('you must be logged in, or create an account if you dont have one')
            return redirect(url_for('login'))

        if 'user' in session:
            is_auth = True

        name = request.args.get('name')
        item_name = request.args.get('item_name')
        shl_items = get_shl(name).get('shl').items
        for item in shl_items:
            if item.name == item_name:
                shl_items.remove(item)
                flash(u"Success!! Item succesfully removed", 'success')

        return redirect(url_for('shopping-list-detail', name=name))


class AboutView(View):
    """About view"""

    methods = ['GET']

    def dispatch_request(self):
        return render_template('flatpages/about.html', title='About')