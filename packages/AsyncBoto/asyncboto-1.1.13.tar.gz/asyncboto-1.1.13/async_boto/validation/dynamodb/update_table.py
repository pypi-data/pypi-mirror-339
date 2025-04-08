from typing import Literal

from pydantic import BaseModel, constr

from .data_types.attribute_definition import AttributeDefinition
from .data_types.global_secondary_index_update import GlobalSecondaryIndexUpdate
from .data_types.on_demand_throughput import (
    OnDemandThroughput as OnDemandThroughputModel,
)
from .data_types.provisioned_throughput import (
    ProvisionedThroughput as ProvisionedThroughputModel,
)
from .data_types.replication_group_update import ReplicationGroupUpdate
from .data_types.sse_specification import SSESpecification as SSESpecificationModel
from .data_types.stream_specification import (
    StreamSpecification as StreamSpecificationModel,
)
from .data_types.table_description import TableDescription as TableDescriptionModel
from .data_types.warm_throughput import WarmThroughput as WarmThroughputModel


class UpdateTableRequest(BaseModel):
    """
    Request model for the UpdateTable operation.

    Attributes
    ----------
    TableName : constr(min_length=1, max_length=1024)
        The name of the table to be updated.
    AttributeDefinitions : Optional[List[AttributeDefinition]]
        An array of attributes that describe the key schema for the table and indexes.
    BillingMode : Optional[Literal["PROVISIONED", "PAY_PER_REQUEST"]]
        Controls how you are charged for read and write throughput.
    DeletionProtectionEnabled : Optional[bool]
        Indicates whether deletion protection is enabled.
    GlobalSecondaryIndexUpdates : Optional[List[GlobalSecondaryIndexUpdate]]
        An array of one or more global secondary indexes for the table.
    MultiRegionConsistency : Optional[Literal["EVENTUAL", "STRONG"]]
        Specifies the consistency mode for a new global table.
    OnDemandThroughput : Optional[OnDemandThroughput]
        Updates the maximum number of read and write units for the specified table in
        on-demand capacity mode.
    ProvisionedThroughput : Optional[ProvisionedThroughput]
        The new provisioned throughput settings for the specified table or index.
    ReplicaUpdates : Optional[List[ReplicationGroupUpdate]]
        A list of replica update actions for the table.
    SSESpecification : Optional[SSESpecification]
        The new server-side encryption settings for the specified table.
    StreamSpecification : Optional[StreamSpecification]
        Represents the DynamoDB Streams configuration for the table.
    TableClass : Optional[Literal["STANDARD", "STANDARD_INFREQUENT_ACCESS"]]
        The table class of the table to be updated.
    WarmThroughput : Optional[WarmThroughput]
        Represents the warm throughput for updating a table.
    """

    TableName: constr(min_length=1, max_length=1024)
    AttributeDefinitions: list[AttributeDefinition] | None = None
    BillingMode: Literal["PROVISIONED", "PAY_PER_REQUEST"] | None = None
    DeletionProtectionEnabled: bool | None = None
    GlobalSecondaryIndexUpdates: list[GlobalSecondaryIndexUpdate] | None = None
    MultiRegionConsistency: Literal["EVENTUAL", "STRONG"] | None = None
    OnDemandThroughput: OnDemandThroughputModel | None = None
    ProvisionedThroughput: ProvisionedThroughputModel | None = None
    ReplicaUpdates: list[ReplicationGroupUpdate] | None = None
    SSESpecification: SSESpecificationModel | None = None
    StreamSpecification: StreamSpecificationModel | None = None
    TableClass: Literal["STANDARD", "STANDARD_INFREQUENT_ACCESS"] | None = None
    WarmThroughput: WarmThroughputModel | None = None


class UpdateTableResponse(BaseModel):
    """
    Response model for the UpdateTable operation.

    Attributes
    ----------
    TableDescription : Optional[TableDescription]
        Represents the properties of the table.
    """

    TableDescription: TableDescriptionModel | None = None
