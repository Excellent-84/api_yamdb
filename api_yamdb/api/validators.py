import re

from django.core.exceptions import ValidationError


def validate_username(username):
    if username.lower() == 'me':
        raise ValidationError(
            'Использовать логин "me" запрещено'
        )
    if not re.match(r'^[\w.@+-]+\Z', username):
        raise ValidationError('Недопустимые символы в логине')
    return username
