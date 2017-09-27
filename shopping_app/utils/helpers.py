import os
import random
import string
from datetime import date, datetime
import main


def random_name():
    return ''.join([random.choice(string.ascii_lowercase + string.digits) for n in range(20)])


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


def secret_key_gen():
    filepath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/secret.txt'
    generated_key = ''.join([random.SystemRandom().choice(string.ascii_letters + string.digits)
                             for _ in range(50)])
    with open(filepath, 'w') as secret_file:
        secret_file.write(
            '%(key)s' % dict(key=generated_key)
        )

    print('Find your secret key at %(path)s' % dict(path=filepath))


def check_name(name):
    for shl in main.app.shopping_list:
        if shl.get('name') == name:
            return True
    return False


def get_shl(name):
    for shl in main.app.shopping_list:
        if shl.get('name') == name:
            return shl

