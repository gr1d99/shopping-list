from wtforms import Form, DecimalField, IntegerField, StringField, PasswordField, validators, ValidationError
from wtforms.validators import DataRequired, InputRequired
from .utils.helpers import check_duplicate_item_name


class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


class CreateShoppingItemForm(Form):
    item_name = StringField('item-name', validators=[InputRequired()])
    quantity = IntegerField('quantity', validators=[InputRequired()])
    price = DecimalField('price', validators=[InputRequired()])


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=3, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match'),
        validators.Length(min=6)
    ])
    confirm = PasswordField('Repeat Password')


class CreateShoppingListForm(Form):
    name = StringField('name', validators=[InputRequired()])
