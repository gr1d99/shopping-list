"""Contains all needed forms"""

import string
from wtforms import (Form, DecimalField, IntegerField, StringField,
                     PasswordField, validators, BooleanField, ValidationError)
from wtforms.validators import DataRequired, InputRequired

BAD_CHARS = (c for c in string.punctuation)  # bad characters generator


class LoginForm(Form):
    """For to handle login"""
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

    def validate_name(self, field):
        """
        Validate punctuation characters
        :param field:
        :return:
        """
        name = [n for n in field.data]
        for c in BAD_CHARS:
            if c in name:
                raise ValidationError("%(c)s is an invalid name" % dict(c=c))


class CreateShoppingItemForm(Form):
    """A form to handle creation of shopping items"""
    item_name = StringField('item-name', validators=[InputRequired()])
    quantity = IntegerField('quantity', validators=[InputRequired()])
    price = DecimalField('price', validators=[InputRequired()])
    checked = BooleanField('checked')

    def validate_item_name(self, field):
        """
        Validate punctuation characters
        :param field:
        :return:
        """
        name = [n for n in field.data]
        for c in BAD_CHARS:
            if c in name:
                raise ValidationError("%(c)s is an invalid name" % dict(c=c))


class RegistrationForm(Form):
    """A form to handle registration of users"""
    username = StringField('Username', [validators.Length(min=3, max=25)])
    email = StringField('Email Address', [validators.Email(), validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match'),
        validators.Length(min=6)
    ])
    confirm = PasswordField('Repeat Password')

    def validate_username(self, field):
        """
        Validate punctuation characters
        :param field:
        :return:
        """
        name = [n for n in field.data]
        for c in BAD_CHARS:
            if c in name:
                raise ValidationError("%(c)s is an invalid name" % dict(c=c))


class CreateShoppingListForm(Form):
    """A form to handle creation of shopping list"""
    name = StringField('name', validators=[InputRequired()])

    def validate_name(self, field):
        """
        Validate bad characters
        :param field:
        :return:
        """
        name = [n for n in field.data]
        for c in BAD_CHARS:
            if c in name:
                raise ValidationError("%(c)s is an invalid name" % dict(c=c))
