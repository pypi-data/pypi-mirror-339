from pydantic import BaseModel, conlist

from .attribute_value import AttributeValueDict


class ItemCollectionMetrics(BaseModel):
    """
    Information about item collections, if any, that were affected by the operation.

    Attributes
    ----------
    ItemCollectionKey : Optional[Dict[str, AttributeValue]]
        The partition key value of the item collection.
    SizeEstimateRangeGB : Optional[List[float]]
        An estimate of item collection size, in gigabytes.
    """

    ItemCollectionKey: AttributeValueDict | None = None
    SizeEstimateRangeGB: conlist(float, min_length=2, max_length=2) | None = None
