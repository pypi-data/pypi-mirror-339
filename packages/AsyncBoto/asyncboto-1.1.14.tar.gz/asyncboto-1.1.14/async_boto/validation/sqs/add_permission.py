from pydantic import BaseModel, constr


class AddPermissionRequest(BaseModel):
    """
    The request accepts the following data in JSON format.

    Attributes
    ----------
    Actions : List[str]
        The action the client wants to allow for the specified principal.
    AWSAccountIds : List[str]
        The AWS account numbers of the principals who are to receive permission.
    Label : str
        The unique identification of the permission you're setting.
    QueueUrl : str
        The URL of the Amazon SQS queue to which permissions are added.
    """

    Actions: list[str]
    AWSAccountIds: list[str]
    Label: constr(max_length=80, pattern=r"^[a-zA-Z0-9-_]+$")
    QueueUrl: str


class AddPermissionResponse(BaseModel):
    """
    Represents an empty HTTP body for a successful AddPermission action response.
    """

    pass
