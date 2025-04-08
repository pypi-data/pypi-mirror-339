from pydantic import BaseModel

from .backup_details import BackupDetails as BackupDetailsModel
from .source_table_details import SourceTableDetails as SourceTableDetailsModel
from .source_table_feature_details import (
    SourceTableFeatureDetails as SourceTableFeatureDetailsModel,
)


class BackupDescription(BaseModel):
    """
    Contains the description of the backup created for the table.

    Attributes
    ----------
    BackupDetails : Optional[BackupDetails]
        Contains the details of the backup created for the table.
    SourceTableDetails : Optional[SourceTableDetails]
        Contains the details of the table when the backup was created.
    SourceTableFeatureDetails : Optional[SourceTableFeatureDetails]
        Contains the details of the features enabled on the table when the backup
        was created. For example, LSIs, GSIs, streams, TTL.
    """

    BackupDetails: BackupDetailsModel | None = None
    SourceTableDetails: SourceTableDetailsModel | None = None
    SourceTableFeatureDetails: SourceTableFeatureDetailsModel | None = None
