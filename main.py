"""where flask instance is created"""

import waitress
import os
from flask import Flask
from shopping_app.db.shopping_list.shopping import ShoppingItem
from shopping_app.db.managers.manager import UserManager
from shopping_app.views import (AboutView, IndexView, CreateShoppingListView,
                                DashboardView, UpdateShoppingListView,
                                LoginView, LogoutView, RegisterView,
                                RemoveShoppingListView, UpdateShoppingItemView,
                                ShoppingListDetailView, RemoveShoppingItemView)

BASEDIR = os.path.dirname(os.path.abspath(__file__))

APP = Flask(__name__)
APP.template_folder = os.path.join(BASEDIR, 'shopping_app/templates')
APP.static_folder = os.path.join(BASEDIR, 'shopping_app/static')
APP.user_manager = UserManager()  # user manager instance
APP.shopping_item = ShoppingItem  # initialize shopping item
APP.shopping_list = []  # create an empty list that will hold shopping list instances
APP_USERS = []

# app urls
APP.add_url_rule('/',
                 view_func=IndexView.as_view('index'))
APP.add_url_rule('/dashboard',
                 view_func=DashboardView.as_view('dashboard'))
APP.add_url_rule('/login',
                 view_func=LoginView.as_view('login'))
APP.add_url_rule('/logout',
                 view_func=LogoutView.as_view('logout'))
APP.add_url_rule('/register',
                 view_func=RegisterView.as_view('register'))
APP.add_url_rule('/create-shopping-list',
                 view_func=CreateShoppingListView.as_view('create-shopping-list'))
APP.add_url_rule('/shopping-list-detail/',
                 view_func=ShoppingListDetailView.as_view('shopping-list-detail'))
APP.add_url_rule('/remove-shopping-list/',
                 view_func=RemoveShoppingListView.as_view('remove-shopping-list'))
APP.add_url_rule('/remove-shopping-item/',
                 view_func=RemoveShoppingItemView.as_view('remove-shopping-item'))
APP.add_url_rule('/update-item/',
                 view_func=UpdateShoppingItemView.as_view('update-item'))
APP.add_url_rule('/update-shopping-list/',
                 view_func=UpdateShoppingListView.as_view('update-shopping-list'))

APP.add_url_rule('/about',
                 view_func=AboutView.as_view('about'))

# app conf
APP.debug = True
APP.secret_key = os.environ.get('SECRET_KEY')


if __name__ == '__main__':
    waitress.serve(APP)
