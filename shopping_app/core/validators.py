"""a module contains custom form validators"""

import string

from wtforms import ValidationError


BAD_CHARS = list(string.punctuation)  # list all punctuations


def validate_names(form, field):
    """
    Validate punctuation characters
    """
    data = field.data
    user_data = (char for char in data)  # submitted data generator
    for char in user_data:  # iterate over each character
        if char in BAD_CHARS:  # check if each character is in punctuation list
            raise ValidationError("%(data)s is an invalid name" % dict(data=data))
