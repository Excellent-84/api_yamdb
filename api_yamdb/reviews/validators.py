import re
from datetime import datetime

from django.core.exceptions import ValidationError

from api_yamdb.settings import RESERVED_NAMES, REGULAR_CHECK_LOGIN_VALID


def validate_year(value):
    year = datetime.now().year
    if value > year:
        raise ValidationError('Проверьте год выпуска!')
    return value


def validate_username(username):
    if username.lower() in RESERVED_NAMES:
        raise ValidationError(
            'Зарезервированный логин, нельзя использлвать'
        )
    if not re.match(REGULAR_CHECK_LOGIN_VALID, username):
        raise ValidationError(
            'В логине нельзя использовать символы, отличные от букв'
            'в верхнем и нижнем регистрах, цифр, знаков подчеркивания,'
            'точки, знаков плюса, минуса и собаки (@)'
        )
    return username
