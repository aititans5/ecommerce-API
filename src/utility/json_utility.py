import datetime
def json_default(value):
    if isinstance(value, datetime.date):
        return str(value)
    else:
        return value.__dict__
