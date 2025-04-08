from pydantic import BaseModel, constr


class Tag(BaseModel):
    """
    Describes a tag. A tag is a key-value pair. You can add up to 50 tags to a single
    DynamoDB table.

    Attributes
    ----------
    Key : constr(min_length=1, max_length=128)
        The key of the tag. Tag keys are case sensitive.
    Value : constr(min_length=0, max_length=256)
        The value of the tag. Tag values are case-sensitive and can be null.
    """

    Key: constr(min_length=1, max_length=128)
    Value: constr(min_length=0, max_length=256)
