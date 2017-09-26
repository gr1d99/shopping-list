from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms.validators import DataRequired, InputRequired


class LoginForm(Form):
    username = StringField('username', validators=[InputRequired(), DataRequired()])
    password = PasswordField('password', validators=[InputRequired(), DataRequired()])


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
