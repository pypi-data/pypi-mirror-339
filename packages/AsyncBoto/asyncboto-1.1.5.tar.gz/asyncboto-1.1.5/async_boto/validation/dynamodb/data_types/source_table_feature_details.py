from pydantic import BaseModel

from .global_secondary_index_info import GlobalSecondaryIndexInfo
from .local_secondary_index_info import LocalSecondaryIndexInfo
from .sse_description import SSEDescription as SSEDescriptionModel
from .stream_specification import StreamSpecification as StreamSpecificationModel
from .time_to_live_description import (
    TimeToLiveDescription as TimeToLiveDescriptionModel,
)


class SourceTableFeatureDetails(BaseModel):
    """
    Contains the details of the features enabled on the table when the backup was
    created.
    For example, LSIs, GSIs, streams, TTL.

    Attributes
    ----------
    GlobalSecondaryIndexes : Optional[List[GlobalSecondaryIndexInfo]]
        Represents the GSI properties for the table when the backup was created.
    LocalSecondaryIndexes : Optional[List[LocalSecondaryIndexInfo]]
        Represents the LSI properties for the table when the backup was created.
    SSEDescription : Optional[SSEDescription]
        The description of the server-side encryption status on the table when the
        backup was created.
    StreamDescription : Optional[StreamSpecification]
        Stream settings on the table when the backup was created.
    TimeToLiveDescription : Optional[TimeToLiveDescription]
        Time to Live settings on the table when the backup was created.
    """

    GlobalSecondaryIndexes: list[GlobalSecondaryIndexInfo] | None = None
    LocalSecondaryIndexes: list[LocalSecondaryIndexInfo] | None = None
    SSEDescription: SSEDescriptionModel | None = None
    StreamDescription: StreamSpecificationModel | None = None
    TimeToLiveDescription: TimeToLiveDescriptionModel | None = None
