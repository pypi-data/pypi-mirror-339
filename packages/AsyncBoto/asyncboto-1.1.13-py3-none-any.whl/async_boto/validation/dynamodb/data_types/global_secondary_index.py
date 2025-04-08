from pydantic import BaseModel, constr

from .key_schema_element import KeySchemaElement
from .on_demand_throughput import OnDemandThroughput as OnDemandThroughputModel
from .projection import Projection as ProjectionModel
from .provisioned_throughput import ProvisionedThroughput as ProvisionedThroughputModel
from .warm_throughput import WarmThroughput as WarmThroughputModel


class GlobalSecondaryIndex(BaseModel):
    """
    Represents the properties of a global secondary index.

    Attributes
    ----------
    IndexName : constr(min_length=3, max_length=255, regex=r'[a-zA-Z0-9_.-]+')
        The name of the global secondary index. The name must be unique among all
        other indexes on this table.
    KeySchema : List[KeySchemaElement]
        The complete key schema for a global secondary index, which consists of one
        or more pairs of attribute names and key types.
    Projection : Projection
        Represents attributes that are copied (projected) from the table into the
        global secondary index.
    OnDemandThroughput : Optional[OnDemandThroughput]
        The maximum number of read and write units for the specified global
        secondary index.
    ProvisionedThroughput : Optional[ProvisionedThroughput]
        Represents the provisioned throughput settings for the specified global
        secondary index.
    WarmThroughput : Optional[WarmThroughput]
        Represents the warm throughput value (in read units per second and write units
        per second) for the specified secondary index.
    """

    IndexName: constr(min_length=3, max_length=255, pattern=r"[a-zA-Z0-9_.-]+")
    KeySchema: list[KeySchemaElement]
    Projection: ProjectionModel
    OnDemandThroughput: OnDemandThroughputModel | None = None
    ProvisionedThroughput: ProvisionedThroughputModel | None = None
    WarmThroughput: WarmThroughputModel | None = None
