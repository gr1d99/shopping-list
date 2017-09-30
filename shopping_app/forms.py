"""Contains all needed forms"""

from wtforms import (Form, DecimalField, IntegerField, StringField,
                     PasswordField, validators, BooleanField, ValidationError)
from wtforms.validators import DataRequired, InputRequired
from .core.validators import validate_names


class LoginForm(Form):
    """For to handle login"""
    username = StringField('username', validators=[DataRequired(), validate_names])
    password = PasswordField('password', validators=[DataRequired()])


class CreateShoppingItemForm(Form):
    """A form to handle creation of shopping items"""
    item_name = StringField('item-name', validators=[validate_names, InputRequired()])
    quantity = IntegerField('quantity', validators=[InputRequired()])
    price = DecimalField('price', validators=[InputRequired()])
    checked = BooleanField('checked')


class RegistrationForm(Form):
    """A form to handle registration of users"""
    username = StringField('Username', [validators.Length(min=3, max=25), validate_names])
    email = StringField('Email Address', [validators.Email(), validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match'),
        validators.Length(min=6)
    ])
    confirm = PasswordField('Repeat Password')


class CreateShoppingListForm(Form):
    """A form to handle creation of shopping list"""
    name = StringField('name', validators=[InputRequired(), validate_names])
