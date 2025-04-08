from pydantic import BaseModel, conint


class ProvisionedThroughput(BaseModel):
    """
    Represents the provisioned throughput settings for a specified table or index.

    Attributes
    ----------
    ReadCapacityUnits : int
        The maximum number of strongly consistent reads consumed per second before
        DynamoDB returns a ThrottlingException.
    WriteCapacityUnits : int
        The maximum number of writes consumed per second before DynamoDB returns a
        ThrottlingException.
    """

    ReadCapacityUnits: conint(ge=0)
    WriteCapacityUnits: conint(ge=0)
