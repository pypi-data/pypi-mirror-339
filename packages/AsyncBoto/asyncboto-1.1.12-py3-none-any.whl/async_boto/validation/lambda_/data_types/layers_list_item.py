from pydantic import BaseModel

from .layer_versions_list_item import LayerVersionsListItem


class LayersListItem(BaseModel):
    """
    Details about an AWS Lambda layer.

    Parameters
    ----------
    LatestMatchingVersion : Optional[LayerVersionsListItem]
        The newest version of the layer.
    LayerArn : Optional[str]
        The Amazon Resource Name (ARN) of the function layer.
    LayerName : Optional[str]
        The name of the layer.
    """

    LatestMatchingVersion: LayerVersionsListItem | None = None
    LayerArn: str | None = None
    LayerName: str | None = None
