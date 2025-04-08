from pydantic import BaseModel, constr


class TagsError(BaseModel):
    """
    An object that contains details about an error related to retrieving tags.

    Attributes
    ----------
    ErrorCode : constr
        The error code.
    Message : constr
        The error message.
    """

    ErrorCode: constr(min_length=10, max_length=21, pattern=r"[A-Za-z]+Exception")
    Message: constr(min_length=84, max_length=1000, pattern=r"^.*$")
