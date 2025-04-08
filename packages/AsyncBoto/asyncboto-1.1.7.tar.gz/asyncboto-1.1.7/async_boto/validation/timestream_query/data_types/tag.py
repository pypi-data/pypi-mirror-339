from pydantic import BaseModel, Field


class Tag(BaseModel):
    """
    A tag is a label that you assign to a Timestream database and/or table. Each
    tag consists of a key and an optional value, both of which you define. Tags
    enable you to categorize databases and/or tables, for example, by purpose,
    owner, or environment.

    Parameters
    ----------
    Key : str
        The key of the tag. Tag keys are case sensitive.
    Value : str
        The value of the tag. Tag values are case sensitive and can be null.
    """

    Key: str = Field(min_length=1, max_length=128)
    Value: str = Field(min_length=0, max_length=256)
