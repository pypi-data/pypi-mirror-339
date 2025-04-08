from pydantic import BaseModel, constr

from .data_types.time_to_live_description import (
    TimeToLiveDescription as TimeToLiveDescriptionModel,
)


class DescribeTimeToLiveRequest(BaseModel):
    """
    Gives a description of the Time to Live (TTL) status on the specified table.

    Attributes
    ----------
    TableName : str
        The name of the table to be described. You can also provide the Amazon
        Resource Name (ARN) of the table in this parameter.
    """

    TableName: constr(min_length=1, max_length=1024)


class DescribeTimeToLiveResponse(BaseModel):
    """
    Response for the DescribeTimeToLive operation.

    Attributes
    ----------
    TimeToLiveDescription : Optional[TimeToLiveDescription]
        Represents the Time to Live (TTL) status of the table.
    """

    TimeToLiveDescription: TimeToLiveDescriptionModel | None = None
