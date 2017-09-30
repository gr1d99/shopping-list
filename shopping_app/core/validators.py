"""a module contains custom form validators"""

import string

from wtforms import ValidationError


BAD_CHARS = (c for c in string.punctuation)  # bad characters generator


def validate_names(form, field):
    """
    Validate punctuation characters
    :param form:
    :param field:
    :return:
    """
    data = field.data
    data_list = list(data)  # list supplied data so that it allows the use of `in` statement
    for pun in BAD_CHARS:  # iterate over bad characters
        if pun in data_list:  # check if punctuation is in supplied data
            raise ValidationError("%(data)s is an invalid name" % dict(data=data))
