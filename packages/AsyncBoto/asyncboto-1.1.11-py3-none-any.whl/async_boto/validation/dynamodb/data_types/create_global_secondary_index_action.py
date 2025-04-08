from pydantic import BaseModel, conlist, constr

from .key_schema_element import KeySchemaElement
from .on_demand_throughput import OnDemandThroughput as OnDemandThroughputModel
from .projection import Projection as ProjectionModel
from .provisioned_throughput import ProvisionedThroughput as ProvisionedThroughputModel
from .warm_throughput import WarmThroughput as WarmThroughputModel


class CreateGlobalSecondaryIndexAction(BaseModel):
    """
    Represents a new global secondary index to be added to an existing table.

    Attributes
    ----------
    IndexName : constr(min_length=3, max_length=255, pattern=r"[a-zA-Z0-9_.-]+")
        The name of the global secondary index to be created.
    KeySchema : conlist(KeySchemaElement, min_items=1, max_items=2)
        The key schema for the global secondary index.
    Projection : ProjectionModel
        Represents attributes that are copied (projected) from the table into an index.
    OnDemandThroughput : Optional[OnDemandThroughputModel]
        The maximum number of read and write units for the global secondary index
        being created.
    ProvisionedThroughput : Optional[ProvisionedThroughputModel]
        Represents the provisioned throughput settings for the specified global
        secondary index.
    WarmThroughput : Optional[WarmThroughputModel]
        Represents the warm throughput value (in read units per second and write units
        per second) when creating a secondary index.
    """

    IndexName: constr(min_length=3, max_length=255, pattern=r"[a-zA-Z0-9_.-]+")
    KeySchema: conlist(KeySchemaElement, min_length=1, max_length=2)
    Projection: ProjectionModel
    OnDemandThroughput: OnDemandThroughputModel | None = None
    ProvisionedThroughput: ProvisionedThroughputModel | None = None
    WarmThroughput: WarmThroughputModel | None = None
