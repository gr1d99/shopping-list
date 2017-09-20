from functools import wraps
from flask import flash, redirect, render_template, request, session, url_for
from flask.views import View


def check_shoppinglist(func):
    @wraps(func)
    def _wrapped(view):
        my_shopping_list = session.get('shopping_list', {})
        if not my_shopping_list:
            flash('You do not have any shopping list, add some through your dashboard')
        return func(view)
    return _wrapped


class IndexView(View):
    methods = ['GET', ]

    @check_shoppinglist
    def dispatch_request(self):
        my_shopping_list = session.get('shopping_list', {})
        return render_template('index.html', shopping_list=my_shopping_list)


class DashboardView(View):
    methods = ['GET', ]

    @check_shoppinglist
    def dispatch_request(self):
        my_shopping_list = session.get('shopping_list', {})
        return render_template('dashboard.html', shopping_list=my_shopping_list)


class LoginView(View):
    methods = ['GET', 'POST']

    def dispatch_request(self):
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            session['users'] = {}
            session.get('users').update({'username': username, 'password': password})
            flash('You are logged in')
            return redirect(url_for('index'))

        return render_template('login.html')


class RegisterView(View):
    def dispatch_request(self):
        return render_template('register.html')


class AddItemsView(View):
    methods = ['GET', 'POST']

    def dispatch_request(self):
        if request.method == 'POST':
            if 'shopping_list' not in session:
                session['shopping_list'] = {}

            shopping_list_name = request.form.get('name')
            item_names = ['item1', 'item2', 'item3']
            items = [request.form.get(item) for item in item_names]
            session['shopping_list'].update({shopping_list_name: items})
            flash('Sucess!, you items are %(items)s, to view them go to your dashboard' % dict(items=session['shopping_list']))

            return redirect(url_for('create-shopping-list'))
        return render_template('shopping_list/create_shopping_list.html')


class ShoppingListDetail(View):
    methods = ['GET', ]

    def dispatch_request(self):
        if 'shopping_list' not in session:
            flash('There seems not to be anything in your shopping list')
            return redirect(url_for('dashboard'))

        list_name = request.args.get('name')
        shopping_list_obj = session['shopping_list'].get(list_name, None)

        if not shopping_list_obj:
            flash('Oops it looks like your shopping list does not exist.')
            return redirect(url_for('dashboard'))

        return render_template('shopping_list/shopping_list_detail.html', list_name=list_name, obj=shopping_list_obj)


class RemoveSingleItem(View):
    methods = ['POST', ]

    def dispatch_request(self):
        shopping_list = request.form['shopping_list_name']
        item_name = request.form['item_name']

        user_shopping_list = session['shopping_list']
        target_shopping_list = user_shopping_list.get(shopping_list)
        flash(target_shopping_list)
        return redirect(url_for('dashboard'))