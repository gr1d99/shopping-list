import configparser
import os
from flask import Flask
from views import (IndexView, AddItemsView, DashboardView,
                   LoginView, Logout, RegisterView,
                   RemoveShoppingList, ShoppingListDetail)

BASEDIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
config = configparser.ConfigParser()
config.read(BASEDIR + '/secret.ini')

# app urls
app.add_url_rule('/', view_func=IndexView.as_view('index'))
app.add_url_rule('/dashboard', view_func=DashboardView.as_view('dashboard'))
app.add_url_rule('/login', view_func=LoginView.as_view('login'))
app.add_url_rule('/logout', view_func=Logout.as_view('logout'))
app.add_url_rule('/register', view_func=RegisterView.as_view('register'))
app.add_url_rule('/create-shopping-list', view_func=AddItemsView.as_view('create-shopping-list'))
app.add_url_rule('/shopping-list-detail/', view_func=ShoppingListDetail.as_view('shopping-list-detail'))
app.add_url_rule('/remove-shopping-list', view_func=RemoveShoppingList.as_view('remove-shopping-list'))

# app conf
app.secret_key = config['SECRET_KEY']['KEY']


if __name__ == '__main__':
    app.run()
