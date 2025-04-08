from typing import Literal

from pydantic import BaseModel, constr

from .data_types.attribute_definition import AttributeDefinition
from .data_types.global_secondary_index import GlobalSecondaryIndex
from .data_types.key_schema_element import KeySchemaElement
from .data_types.local_secondary_index import LocalSecondaryIndex
from .data_types.on_demand_throughput import (
    OnDemandThroughput as OnDemandThroughputModel,
)
from .data_types.provisioned_throughput import (
    ProvisionedThroughput as ProvisionedThroughputModel,
)
from .data_types.sse_specification import SSESpecification as SSESpecificationModel
from .data_types.stream_specification import (
    StreamSpecification as StreamSpecificationModel,
)
from .data_types.table_description import TableDescription as TableDescriptionModel
from .data_types.tag import Tag
from .data_types.warm_throughput import WarmThroughput as WarmThroughputModel


class CreateTableRequest(BaseModel):
    """
    Creates a new table in DynamoDB.

    Attributes
    ----------
    AttributeDefinitions : List[AttributeDefinition]
        An array of attributes that describe the key schema for the table and indexes.
    KeySchema : List[KeySchemaElement]
        Specifies the attributes that make up the primary key for a table or an index.
    TableName : str
        The name of the table to create.
    BillingMode : Optional[Literal['PROVISIONED', 'PAY_PER_REQUEST']]
        Controls how you are charged for read and write throughput and how you manage
        capacity.
    DeletionProtectionEnabled : Optional[bool]
        Indicates whether deletion protection is to be enabled (true) or
        disabled (false) on the table.
    GlobalSecondaryIndexes : Optional[List[GlobalSecondaryIndex]]
        One or more global secondary indexes to be created on the table.
    LocalSecondaryIndexes : Optional[List[LocalSecondaryIndex]]
        One or more local secondary indexes to be created on the table.
    OnDemandThroughput : Optional[OnDemandThroughput]
        Sets the maximum number of read and write units for the specified table in
        on-demand capacity mode.
    ProvisionedThroughput : Optional[ProvisionedThroughput]
        Represents the provisioned throughput settings for a specified table or index.
    ResourcePolicy : Optional[str]
        An AWS resource-based policy document in JSON format that will be attached
        to the table.
    SSESpecification : Optional[SSESpecification]
        Represents the settings used to enable server-side encryption.
    StreamSpecification : Optional[StreamSpecification]
        The settings for DynamoDB Streams on the table.
    TableClass : Optional[Literal['STANDARD', 'STANDARD_INFREQUENT_ACCESS']]
        The table class of the new table.
    Tags : Optional[List[Tag]]
        A list of key-value pairs to label the table.
    WarmThroughput : Optional[WarmThroughput]
        Represents the warm throughput for creating a table.
    """

    AttributeDefinitions: list[AttributeDefinition]
    KeySchema: list[KeySchemaElement]
    TableName: constr(min_length=1, max_length=1024)
    BillingMode: Literal["PROVISIONED", "PAY_PER_REQUEST"] | None = None
    DeletionProtectionEnabled: bool | None = None
    GlobalSecondaryIndexes: list[GlobalSecondaryIndex] | None = None
    LocalSecondaryIndexes: list[LocalSecondaryIndex] | None = None
    OnDemandThroughput: OnDemandThroughputModel | None = None
    ProvisionedThroughput: ProvisionedThroughputModel | None = None
    ResourcePolicy: str | None = None
    SSESpecification: SSESpecificationModel | None = None
    StreamSpecification: StreamSpecificationModel | None = None
    TableClass: Literal["STANDARD", "STANDARD_INFREQUENT_ACCESS"] | None = None
    Tags: list[Tag] | None = None
    WarmThroughput: WarmThroughputModel | None = None


class CreateTableResponse(BaseModel):
    """
    Represents the output of a CreateTable operation.

    Attributes
    ----------
    TableDescription : dict
        Represents the properties of the table.
    """

    TableDescription: TableDescriptionModel
