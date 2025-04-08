from datetime import datetime
from typing import Literal

from pydantic import BaseModel, constr

from .data_types.global_secondary_index import GlobalSecondaryIndex
from .data_types.local_secondary_index import LocalSecondaryIndex
from .data_types.on_demand_throughput import OnDemandThroughput
from .data_types.provisioned_throughput import ProvisionedThroughput
from .data_types.sse_specification import SSESpecification
from .data_types.table_description import TableDescription as TableDescriptionModel


class RestoreTableToPointInTimeRequest(BaseModel):
    """
    Request model for the RestoreTableToPointInTime operation.

    Attributes
    ----------
    TargetTableName : str
        The name of the new table to which it must be restored to.
    BillingModeOverride : Optional[str]
        The billing mode of the restored table.
    GlobalSecondaryIndexOverride : Optional[List[GlobalSecondaryIndex]]
        List of global secondary indexes for the restored table.
    LocalSecondaryIndexOverride : Optional[List[LocalSecondaryIndex]]
        List of local secondary indexes for the restored table.
    OnDemandThroughputOverride : Optional[OnDemandThroughput]
        Sets the maximum number of read and write units for the specified
        on-demand table.
    ProvisionedThroughputOverride : Optional[ProvisionedThroughput]
        Provisioned throughput settings for the restored table.
    RestoreDateTime : Optional[datetime]
        Time in the past to restore the table to.
    SourceTableArn : Optional[str]
        The DynamoDB table that will be restored.
    SourceTableName : Optional[str]
        Name of the source table that is being restored.
    SSESpecificationOverride : Optional[SSESpecification]
        The new server-side encryption settings for the restored table.
    UseLatestRestorableTime : Optional[bool]
        Restore the table to the latest possible time.
    """

    TargetTableName: constr(min_length=3, max_length=255, pattern=r"[a-zA-Z0-9_.-]+")
    BillingModeOverride: Literal["PROVISIONED", "PAY_PER_REQUEST"] | None = None
    GlobalSecondaryIndexOverride: list[GlobalSecondaryIndex] | None = None
    LocalSecondaryIndexOverride: list[LocalSecondaryIndex] | None = None
    OnDemandThroughputOverride: OnDemandThroughput | None = None
    ProvisionedThroughputOverride: ProvisionedThroughput | None = None
    RestoreDateTime: datetime | None = None
    SourceTableArn: constr(min_length=1, max_length=1024) | None = None
    SourceTableName: (
        constr(min_length=3, max_length=255, pattern=r"[a-zA-Z0-9_.-]+") | None
    ) = None  # noqa: E501
    SSESpecificationOverride: SSESpecification | None = None
    UseLatestRestorableTime: bool | None = None


class RestoreTableToPointInTimeResponse(BaseModel):
    """
    Response model for the RestoreTableToPointInTime operation.

    Attributes
    ----------
    TableDescription : TableDescription
        Represents the properties of a table.
    """

    TableDescription: TableDescriptionModel
