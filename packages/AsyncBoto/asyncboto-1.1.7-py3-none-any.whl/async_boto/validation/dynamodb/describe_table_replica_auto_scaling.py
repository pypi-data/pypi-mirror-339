from pydantic import BaseModel, constr

from .data_types.table_auto_scaling_description import (
    TableAutoScalingDescription as TableAutoScalingDescriptionModel,
)


class DescribeTableReplicaAutoScalingRequest(BaseModel):
    """
    Describes auto scaling settings across replicas of the global table at once.

    Attributes
    ----------
    TableName : str
        The name of the table. You can also provide the Amazon Resource Name (ARN)
        of the table in this parameter.
    """

    TableName: constr(min_length=1, max_length=1024)


class DescribeTableReplicaAutoScalingResponse(BaseModel):
    """
    Response for the DescribeTableReplicaAutoScaling operation.

    Attributes
    ----------
    TableAutoScalingDescription : Optional[TableAutoScalingDescription]
        Represents the auto scaling properties of the table.
    """

    TableAutoScalingDescription: TableAutoScalingDescriptionModel | None = None
