import datetime

import pytz

MOSCOW_TIMEZONE = pytz.timezone("Europe/Moscow")

WEEKDAYS_AMOUNT = 7


def now():
    return datetime.datetime.now(tz=MOSCOW_TIMEZONE)


def get_amount_of_days_to_a_weekday(
        current_weekday_index: int, future_weekday_index: int):
    """
    How many days I need to add to get a future_weekday, starting at
    current_weekday
    """
    return (future_weekday_index - current_weekday_index) % WEEKDAYS_AMOUNT
