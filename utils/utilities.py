from datetime import datetime


def validate_date(date):
    date_format = '%Y-%m-%d'

    try:
        datetime.strptime(date, date_format)
        return True
    except ValueError:
        return False
