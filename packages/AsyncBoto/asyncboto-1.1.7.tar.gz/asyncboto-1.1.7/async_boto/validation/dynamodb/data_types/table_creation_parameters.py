from typing import Literal

from pydantic import BaseModel, constr

from .attribute_definition import AttributeDefinition
from .global_secondary_index import GlobalSecondaryIndex
from .key_schema_element import KeySchemaElement
from .on_demand_throughput import OnDemandThroughput as OnDemandThroughputModel
from .provisioned_throughput import ProvisionedThroughput as ProvisionedThroughputModel
from .sse_specification import SSESpecification as SSESpecificationModel


class TableCreationParameters(BaseModel):
    """
    The parameters for the table created as part of the import operation.

    Attributes
    ----------
    AttributeDefinitions : List[AttributeDefinition]
        The attributes of the table created as part of the import operation.
    KeySchema : List[KeySchemaElement]
        The primary key and option sort key of the table created as part of the
        import operation.
    TableName : constr(min_length=3, max_length=255, regex=r"^[a-zA-Z0-9_.-]+$")
        The name of the table created as part of the import operation.
    BillingMode : Optional[Literal['PROVISIONED', 'PAY_PER_REQUEST']]
        The billing mode for provisioning the table created as part of the import
        operation.
    GlobalSecondaryIndexes : Optional[List[GlobalSecondaryIndex]]
        The Global Secondary Indexes (GSI) of the table to be created as part of
        the import operation.
    OnDemandThroughput : Optional[OnDemandThroughput]
        Sets the maximum number of read and write units for the specified
        on-demand table.
    ProvisionedThroughput : Optional[ProvisionedThroughput]
        Represents the provisioned throughput settings for a specified table or index.
    SSESpecification : Optional[SSESpecification]
        Represents the settings used to enable server-side encryption.
    """

    AttributeDefinitions: list[AttributeDefinition]
    KeySchema: list[KeySchemaElement]
    TableName: constr(min_length=3, max_length=255, pattern=r"^[a-zA-Z0-9_.-]+$")
    BillingMode: Literal["PROVISIONED", "PAY_PER_REQUEST"] | None = None
    GlobalSecondaryIndexes: list[GlobalSecondaryIndex] | None = None
    OnDemandThroughput: OnDemandThroughputModel | None = None
    ProvisionedThroughput: ProvisionedThroughputModel | None = None
    SSESpecification: SSESpecificationModel | None = None
