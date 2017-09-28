import datetime

import main
from flask import flash, redirect, render_template, request, session, url_for
from flask.views import View
from .db.models import ShoppingList
from .forms import CreateShoppingItemForm, CreateShoppingListForm, LoginForm, RegistrationForm
from .utils.helpers import (json_serial, check_name, get_shl, check_duplicate_item_name,
                            change_shl_name, check_item, get_item)


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

                main.app.user.create_user(username, password1, email)
                flash(u'Success! you may now login using your username and password', 'success')
                return redirect(url_for('index'))

            flash(u'Please correct the errors below', 'warning')

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

                if main.app.user.validate_user(username, password):
                    session['user'] = username
                    flash(u'Success!! you are now logged in', 'success')
                    return redirect(url_for('index'))

                flash('username or password is incorrect', 'warning')

            flash(u'Please check the errors below', 'warning')

        return render_template('login.html', form=form, title='Login')


class LogoutView(View):

    """A view to logout a user"""

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
        return render_template('index.html', is_auth=is_auth, title='Home Page')


class DashboardView(View):

    """A view to display user dashboard"""

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

        return render_template('dashboard.html', is_auth=is_auth, shopping_lists=shopping_lists, title='Dashboard')


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
            name = form.name.data

            # check if shopping list name exists
            if not check_name(name):
                try:
                    user = main.app.user.get_user(
                        session.get('user')
                    )

                except Exception:
                    main.app.user.create_user(session.get('user'), session.get('user'), '')
                    user = main.app.user.get_user(
                        session.get('user')
                    )
                today = datetime.datetime.now().strftime("%Y-%m-%w")
                shl = ShoppingList()
                shl.create(name, user, today)
                main.app.shopping_list.append({'name': name, 'shl': shl})

                flash(u'Shopping list created', 'success')
                return redirect(url_for('dashboard'))
            flash(u'Shopping list with that name already exists, '
                  u'try another name', 'warning')

        return render_template('shopping_list/create-shopping-list.html', is_auth=is_auth,
                               title='Create Shopping List', form=form)


class ShoppingListDetailView(View):
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
        for item in shl.get('shl').items:
            print(item, item.total_price)

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
            'shopping_list/shopping-list-detail.html',
            obj=shl, form=form, is_auth=is_auth, title=name.capitalize())


class UpdateItemView(View):
    """
    A view to update each individual item
    """
    methods = ['GET', 'POST']

    def dispatch_request(self):
        shopping_list_name = request.args.get('shl_name')
        item_name = request.args.get('item_name')

        return redirect(url_for('shopping-list-detail', name=shopping_list_name))


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
            new_name = form.name.data
            shl = get_shl(name)
            shl.get('shl').update('name', new_name)
            change_shl_name(name, new_name)
            flash(u'Shopping list name changed successfully', 'success')
            return redirect(url_for('dashboard'))

        return render_template('shopping_list/shopping-list-edit.html', form=form)


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

            if not get_shl(shl_name):
                flash(u'The item you are trying to update does not exist, try again', 'warning')
                return redirect(url_for('dashboard'))

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

        if not check_name(name) or not check_item(name, item_name):
            # check if the requested shopping list or item exists
            flash(u'The requested shopping list does not exist', 'warning')
            return redirect(url_for('dashboard'))

        prev_data = {}

        for item in get_shl(name).get('shl').items:
            if item.name == item_name:
                prev_data.update({'name': item.name})
                prev_data.update({'quantity': item.quantity})
                prev_data.update({'price': item.price})
                break

        if not prev_data:
            flash(u'The shopping item you are trying to update does not exist', 'danger')

        form = CreateShoppingItemForm(
            item_name=prev_data.pop('name'),
            quantity=prev_data.pop('quantity'),
            price=prev_data.pop('price')
        )

        if request.method == 'POST':
            form = CreateShoppingItemForm(request.form)
            new_item_name = form.item_name.data
            new_quantity = int(form.quantity.data)
            new_price = float(form.price.data)

            item = get_item(name, item_name)
            if item:
                item.update('name', new_item_name)
                item.update('quantity', new_quantity)
                item.update('price', new_price)
                flash(u'Item successfully updated', 'success')
                return redirect(url_for('shopping-list-detail', name=name))

        return render_template('shopping_list/shopping-item-edit.html', form=form, item_name=item_name,
                               is_auth=is_auth, title='Update %(item)s' % dict(item=item_name))


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