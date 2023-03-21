from datetime import datetime

from django.core.exceptions import ValidationError


def validate_year(value):
    year = datetime.now().year
    if value > year:
        raise ValidationError('Проверьте год выпуска!')
    return value
