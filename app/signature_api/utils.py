import datetime
import uuid


def get_cur_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_unique_str():
    return str(uuid.uuid4()).replace("-", "")
