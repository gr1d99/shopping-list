from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask.views import View


app = Flask(__name__)


class IndexView(View):
    def dispatch_request(self):
        return render_template('index.html')


class DashboardView(View):
    def dispatch_request(self):
        return render_template('dashboard.html')


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

app.add_url_rule('/', view_func=IndexView.as_view('index'))
app.add_url_rule('/dashboard', view_func=DashboardView.as_view('dashboard'))
app.add_url_rule('/login', view_func=LoginView.as_view('login'))
app.add_url_rule('/register', view_func=RegisterView.as_view('register'))
app.secret_key = 'vgcvhevv6edgedgdyegudguygeygdwgydgwdgydgwy'

if __name__ == '__main__':
    app.run()
