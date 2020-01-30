from datetime import datetime


def pretty_datetime(timespec='seconds'):
    return datetime.utcnow().isoformat(timespec='seconds')

