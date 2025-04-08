from pydantic import BaseModel, constr


class GetPolicyRequest(BaseModel):
    """
    Request model for retrieving the resource-based IAM policy for a function, version,
    or alias.

    Attributes
    ----------
    FunctionName : str
        The name or ARN of the Lambda function, version, or alias.
    Qualifier : str
        Specify a version or alias to get the policy for that resource.
    """

    FunctionName: constr(
        min_length=1,
        max_length=170,
        pattern=r"(arn:(aws[a-zA-Z-]*)?:lambda:)?([a-z]{2}(-gov)?-[a-z]+-\d{1}:)?(\d{12}:)?(function:)?([a-zA-Z0-9-_\.]+)(:(\$LATEST|[a-zA-Z0-9-_]+))?",  # noqa: E501
    )
    Qualifier: constr(min_length=1, max_length=128, pattern=r"(|[a-zA-Z0-9$_-]+)")


class GetPolicyResponse(BaseModel):
    """
    Response model for retrieving the resource-based IAM policy for a function, version,
     or alias.

    Attributes
    ----------
    Policy : str
        The resource-based policy.
    RevisionId : str
        A unique identifier for the current revision of the policy.
    """

    Policy: str
    RevisionId: str
