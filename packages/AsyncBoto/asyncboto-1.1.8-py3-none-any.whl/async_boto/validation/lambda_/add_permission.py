# ruff: noqa: E501
from typing import Literal

from pydantic import BaseModel, constr


class AddPermissionRequest(BaseModel):
    """
    Request model for the AddPermission operation.

    Grants a principal permission to use a function.

    Attributes
    ----------
    FunctionName : str
        The name or ARN of the Lambda function, version, or alias.
    Qualifier : Optional[str]
        Specify a version or alias to add permissions to a published version of the function.
    Action : str
        The action that the principal can use on the function.
    EventSourceToken : Optional[str]
        For Alexa Smart Home functions, a token that the invoker must supply.
    FunctionUrlAuthType : Optional[Literal['NONE', 'AWS_IAM']]
        The type of authentication that your function URL uses.
    Principal : str
        The AWS service, AWS account, IAM user, or IAM role that invokes the function.
    PrincipalOrgID : Optional[str]
        The identifier for your organization in AWS Organizations.
    RevisionId : Optional[str]
        Update the policy only if the revision ID matches the ID that's specified.
    SourceAccount : Optional[str]
        For AWS service, the ID of the AWS account that owns the resource.
    SourceArn : Optional[str]
        For AWS services, the ARN of the AWS resource that invokes the function.
    StatementId : str
        A statement identifier that differentiates the statement from others in the same policy.
    """

    FunctionName: constr(
        min_length=1,
        max_length=140,
        pattern=r"(arn:(aws[a-zA-Z-]*)?:lambda:)?([a-z]{2}(-gov)?-[a-z]+-\d{1}:)?(\d{12}:)?(function:)?([a-zA-Z0-9-_]+)(:(\$LATEST|[a-zA-Z0-9-_]+))?",
    )
    Qualifier: (
        constr(min_length=1, max_length=128, pattern=r"(|[a-zA-Z0-9$_-]+)") | None
    ) = None
    Action: constr(pattern=r"(lambda:[*]|lambda:[a-zA-Z]+|[*])")
    EventSourceToken: (
        constr(min_length=0, max_length=256, pattern=r"[a-zA-Z0-9._\-]+") | None
    ) = None
    FunctionUrlAuthType: Literal["NONE", "AWS_IAM"] | None = None
    Principal: constr(pattern=r"[^\s]+")
    PrincipalOrgID: (
        constr(min_length=12, max_length=34, pattern=r"^o-[a-z0-9]{10,32}$") | None
    ) = None
    RevisionId: str | None = None
    SourceAccount: constr(max_length=12, pattern=r"\d{12}") | None = None
    SourceArn: (
        constr(
            pattern=r"arn:(aws[a-zA-Z0-9-]*):([a-zA-Z0-9\-])+:([a-z]{2}(-gov)?-[a-z]+-\d{1})?:(\d{12})?:(.*)"
        )
        | None
    ) = None
    StatementId: constr(min_length=1, max_length=100, pattern=r"([a-zA-Z0-9-_]+)")


class AddPermissionResponse(BaseModel):
    """
    Response model for the AddPermission operation.

    Attributes
    ----------
    Statement : str
        The permission statement that's added to the function policy.
    """

    Statement: str
