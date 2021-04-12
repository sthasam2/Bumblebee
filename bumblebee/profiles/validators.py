import datetime as dt

from django.core.exceptions import ValidationError


def validate_date_lt_today(value):
    if value > dt.datetime.now():
        raise ValidationError(
            f"Datetime can not be greater than present Datetime",
            "\n",
            f"Entered Datetime: {value.strftieme('%d %B, %Y %I:%M%p')}",
            "\n",
            f"Current Datetime: {dt.datetime.now()}",
        )
