from pydantic import BaseModel


class DescribeLimitsResponse(BaseModel):
    """
    Response for the DescribeLimits operation.

    Attributes
    ----------
    AccountMaxReadCapacityUnits : int
        The maximum total read capacity units that your account allows you to provision
        across all of your tables in this Region.
    AccountMaxWriteCapacityUnits : int
        The maximum total write capacity units that your account allows you to provision
        across all of your tables in this Region.
    TableMaxReadCapacityUnits : int
        The maximum read capacity units that your account allows you to provision for
        a new table that you are creating in this Region.
    TableMaxWriteCapacityUnits : int
        The maximum write capacity units that your account allows you to provision for
        a new table that you are creating in this Region.
    """

    AccountMaxReadCapacityUnits: int
    AccountMaxWriteCapacityUnits: int
    TableMaxReadCapacityUnits: int
    TableMaxWriteCapacityUnits: int
