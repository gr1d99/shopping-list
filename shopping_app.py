from flask import Flask
from views import IndexView, AddItemsView, DashboardView, LoginView, RegisterView, RemoveSingleItem, ShoppingListDetail

app = Flask(__name__)


app.add_url_rule('/', view_func=IndexView.as_view('index'))
app.add_url_rule('/dashboard', view_func=DashboardView.as_view('dashboard'))
app.add_url_rule('/login', view_func=LoginView.as_view('login'))
app.add_url_rule('/register', view_func=RegisterView.as_view('register'))
app.add_url_rule('/create-shopping-list', view_func=AddItemsView.as_view('create-shopping-list'))
app.add_url_rule('/shopping-list-detail/', view_func=ShoppingListDetail.as_view('shopping-list-detail'))
app.add_url_rule('/remove-single-item', view_func=RemoveSingleItem.as_view('remove-single-item'))

app.secret_key = 'vgcvhevv6edgedgdyegudguygeygdwgydgwdgydgwy'

if __name__ == '__main__':
    app.run()
