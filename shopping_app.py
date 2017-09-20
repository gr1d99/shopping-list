from flask import Flask
from flask import render_template
from flask.views import View


app = Flask(__name__)


class IndexView(View):
    def dispatch_request(self):
        return render_template('index.html')


class DashboardView(View):
    def dispatch_request(self):
        return render_template('dashboard.html')


class LoginView(View):
    def dispatch_request(self):
        return render_template('login.html')


class RegisterView(View):
    def dispatch_request(self):
        return render_template('register.html')

app.add_url_rule('/', view_func=IndexView.as_view('index'))
app.add_url_rule('/dashboard', view_func=DashboardView.as_view('dashboard'))
app.add_url_rule('/login', view_func=LoginView.as_view('login'))
app.add_url_rule('/register', view_func=RegisterView.as_view('register'))

if __name__ == '__main__':
    app.run()
