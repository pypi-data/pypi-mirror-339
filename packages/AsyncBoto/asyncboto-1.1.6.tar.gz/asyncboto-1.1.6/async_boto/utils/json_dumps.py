import datetime
from typing import Any


def json_dump(obj: Any):
    """
    Custom method, which is used to handle types that cant be handled by
    json.dumps
    """

    if isinstance(obj, datetime.datetime | datetime.date):
        return obj.isoformat()
    raise Exception(f"Type {type(obj)} not serializable")
