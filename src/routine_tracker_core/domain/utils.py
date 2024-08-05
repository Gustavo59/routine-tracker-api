from datetime import date, timedelta


def first_day_of_the_week(date: date):
    return date - timedelta(days=date.weekday())


def first_day_of_the_moth(date: date):
    return date.replace(day=1)


def first_day_of_the_year(date: date):
    return date.replace(day=1, month=1)
