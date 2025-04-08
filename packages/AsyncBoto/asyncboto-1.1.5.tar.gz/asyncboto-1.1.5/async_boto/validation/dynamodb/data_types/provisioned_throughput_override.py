from pydantic import BaseModel, conint


class ProvisionedThroughputOverride(BaseModel):
    """
    Replica-specific provisioned throughput settings. If not specified, uses the source
    table's provisioned throughput settings.

    Attributes
    ----------
    ReadCapacityUnits : Optional[int]
        Replica-specific read capacity units. If not specified, uses the source table's
        read capacity settings.
    """

    ReadCapacityUnits: conint(ge=1) | None = None
