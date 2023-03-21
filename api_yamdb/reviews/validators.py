import re
from datetime import datetime

from django.core.exceptions import ValidationError


def validate_year(value):
    year = datetime.now().year
    if value > year:
        raise ValidationError('Проверьте год выпуска!')
    return value


def validate_username(username):
    if username.lower() == 'me':
        raise ValidationError(
            'Использовать логин "me" запрещено'
        )
    if not re.match(r'^[\w.@+-]+\Z', username):
        raise ValidationError('Недопустимые символы в логине')
    return username
