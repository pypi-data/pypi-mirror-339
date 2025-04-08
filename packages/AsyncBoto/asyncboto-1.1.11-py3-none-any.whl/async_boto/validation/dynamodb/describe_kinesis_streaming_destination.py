from pydantic import BaseModel, constr

from .data_types.kinesis_data_stream_destination import KinesisDataStreamDestination


class DescribeKinesisStreamingDestinationRequest(BaseModel):
    """
    Returns information about the status of Kinesis streaming.

    Attributes
    ----------
    TableName : str
        The name of the table being described. You can also provide the Amazon
        Resource Name (ARN) of the table in this parameter.
    """

    TableName: constr(min_length=1, max_length=1024)


class DescribeKinesisStreamingDestinationResponse(BaseModel):
    """
    Response for the DescribeKinesisStreamingDestination operation.

    Attributes
    ----------
    TableName : str
        The name of the table being described.
    KinesisDataStreamDestinations : List[KinesisDataStreamDestination]
        The list of Kinesis data stream destinations.
    """

    TableName: constr(min_length=3, max_length=255, pattern=r"[a-zA-Z0-9_.-]+")
    KinesisDataStreamDestinations: list[KinesisDataStreamDestination]
