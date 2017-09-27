import os
from flask import Flask
from shopping_app.db.models import User, ShoppingItem
from shopping_app.views import (IndexView, AddItemsView, CreateShoppingList, DashboardView, MarkItemView,
                                LoginView, Logout, RegisterView, RemoveShoppingList, NewShoppingListDetailView)

BASEDIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.template_folder = os.path.join(BASEDIR, 'shopping_app/templates')
app.static_folder = os.path.join(BASEDIR, 'shopping_app/static')
app.user = User()  # user instance
app.shopping_item = ShoppingItem  # initialize shopping item
app.shopping_list = []  # create an empty list that will hold shopping list instances

# app urls
app.add_url_rule('/', view_func=IndexView.as_view('index'))
app.add_url_rule('/dashboard', view_func=DashboardView.as_view('dashboard'))
app.add_url_rule('/login', view_func=LoginView.as_view('login'))
app.add_url_rule('/logout', view_func=Logout.as_view('logout'))
app.add_url_rule('/register', view_func=RegisterView.as_view('register'))
app.add_url_rule('/create-shopping-list', view_func=CreateShoppingList.as_view('create-shopping-list'))
app.add_url_rule('/mark-item', view_func=MarkItemView.as_view('mark-item'))
app.add_url_rule('/shopping-list-detail/', view_func=NewShoppingListDetailView.as_view('shopping-list-detail'))
app.add_url_rule('/remove-shopping-list', view_func=RemoveShoppingList.as_view('remove-shopping-list'))

# app conf
app.debug = True
app.secret_key = os.environ.get('SECRET_KEY')


if __name__ == '__main__':
    app.run()
