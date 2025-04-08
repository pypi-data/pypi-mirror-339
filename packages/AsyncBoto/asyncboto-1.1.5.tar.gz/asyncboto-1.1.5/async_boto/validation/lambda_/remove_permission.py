from pydantic import BaseModel, constr


class RemovePermissionRequest(BaseModel):
    """
    Request model for revoking function-use permission from an AWS service or another
    AWS account.

    Attributes
    ----------
    FunctionName : str
        The name or ARN of the Lambda function, version, or alias.
    StatementId : str
        Statement ID of the permission to remove.
    Qualifier : str
        Specify a version or alias to remove permissions from a published version of
        the function.
    RevisionId : str
        Update the policy only if the revision ID matches the ID that's specified.
    """

    FunctionName: constr(
        min_length=1,
        max_length=140,
        pattern=r"(arn:(aws[a-zA-Z-]*)?:lambda:)?([a-z]{2}(-gov)?-[a-z]+-\d{1}:)?(\d{12}:)?(function:)?([a-zA-Z0-9-_]+)(:(\$LATEST|[a-zA-Z0-9-_]+))?",  # noqa: E501
    )
    StatementId: constr(min_length=1, max_length=100, pattern=r"([a-zA-Z0-9-_.]+)")
    Qualifier: (
        constr(min_length=1, max_length=128, pattern=r"(|[a-zA-Z0-9$_-]+)") | None
    )  # noqa: E501
    RevisionId: str | None


class RemovePermissionResponse(BaseModel):
    """
    Response model for revoking function-use permission from an AWS service or another
    AWS account.

    This is an empty response model as the API returns a 204 No Content status.
    """

    pass
