from pydantic import BaseModel, constr

from .data_types.time_to_live_specification import (
    TimeToLiveSpecification as TimeToLiveSpecificationModel,
)


class UpdateTimeToLiveRequest(BaseModel):
    """
    Request model for the UpdateTimeToLive operation.

    Attributes
    ----------
    TableName : constr(min_length=1, max_length=1024)
        The name of the table to be configured.
    TimeToLiveSpecification : TimeToLiveSpecification
        Represents the settings used to enable or disable Time to Live for the
        specified table.
    """

    TableName: constr(min_length=1, max_length=1024)
    TimeToLiveSpecification: TimeToLiveSpecificationModel


class UpdateTimeToLiveResponse(BaseModel):
    """
    Response model for the UpdateTimeToLive operation.

    Attributes
    ----------
    TimeToLiveSpecification : TimeToLiveSpecification
        Represents the output of an UpdateTimeToLive operation.
    """

    TimeToLiveSpecification: TimeToLiveSpecificationModel
