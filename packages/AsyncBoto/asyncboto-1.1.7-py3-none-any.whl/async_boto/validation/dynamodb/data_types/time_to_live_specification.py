from pydantic import BaseModel, constr


class TimeToLiveSpecification(BaseModel):
    """
    Represents the settings used to enable or disable Time to Live (TTL) for the
    specified table.

    Attributes
    ----------
    AttributeName : constr(min_length=1, max_length=255)
        The name of the TTL attribute used to store the expiration time for items
        in the table.
    Enabled : bool
        Indicates whether TTL is to be enabled (true) or disabled (false) on the table.
    """

    AttributeName: constr(min_length=1, max_length=255)
    Enabled: bool
