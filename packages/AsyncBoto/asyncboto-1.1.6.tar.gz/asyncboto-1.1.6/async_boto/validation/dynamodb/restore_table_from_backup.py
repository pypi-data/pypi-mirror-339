from typing import Literal

from pydantic import BaseModel, constr

from .data_types.global_secondary_index import GlobalSecondaryIndex
from .data_types.local_secondary_index import LocalSecondaryIndex
from .data_types.on_demand_throughput import OnDemandThroughput
from .data_types.provisioned_throughput import ProvisionedThroughput
from .data_types.sse_specification import SSESpecification
from .data_types.table_description import TableDescription as TableDescriptionModel


class RestoreTableFromBackupRequest(BaseModel):
    """
    Request model for the RestoreTableFromBackup operation.

    Attributes
    ----------
    BackupArn : str
        The Amazon Resource Name (ARN) associated with the backup.
    TargetTableName : str
        The name of the new table to which the backup must be restored.
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
    SSESpecificationOverride : Optional[SSESpecification]
        The new server-side encryption settings for the restored table.
    """

    BackupArn: constr(min_length=37, max_length=1024)
    TargetTableName: constr(min_length=3, max_length=255, pattern=r"[a-zA-Z0-9_.-]+")
    BillingModeOverride: Literal["PROVISIONED", "PAY_PER_REQUEST"] | None = None
    GlobalSecondaryIndexOverride: list[GlobalSecondaryIndex] | None = None
    LocalSecondaryIndexOverride: list[LocalSecondaryIndex] | None = None
    OnDemandThroughputOverride: OnDemandThroughput | None = None
    ProvisionedThroughputOverride: ProvisionedThroughput | None = None
    SSESpecificationOverride: SSESpecification | None = None


class RestoreTableFromBackupResponse(BaseModel):
    """
    Response model for the RestoreTableFromBackup operation.

    Attributes
    ----------
    TableDescription : TableDescription
        The description of the table created from an existing backup.
    """

    TableDescription: TableDescriptionModel
