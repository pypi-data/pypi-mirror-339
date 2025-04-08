from pydantic import BaseModel, constr


class GetFunctionCodeSigningConfigRequest(BaseModel):
    """
    Request model for retrieving the code signing configuration for a specified
    function.

    Attributes
    ----------
    FunctionName : str
        The name or ARN of the Lambda function.
    """

    FunctionName: constr(
        min_length=1,
        max_length=140,
        pattern=r"(arn:(aws[a-zA-Z-]*)?:lambda:)?([a-z]{2}(-gov)?-[a-z]+-\d{1}:)?(\d{12}:)?(function:)?([a-zA-Z0-9-_]+)(:(\$LATEST|[a-zA-Z0-9-_]+))?",  # noqa: E501
    )


class GetFunctionCodeSigningConfigResponse(BaseModel):
    """
    Response model for retrieving the code signing configuration for a specified
    function.

    Attributes
    ----------
    CodeSigningConfigArn : str
        The ARN of the code signing configuration.
    FunctionName : str
        The name or ARN of the Lambda function.
    """

    CodeSigningConfigArn: constr(
        max_length=200,
        pattern=r"arn:(aws[a-zA-Z-]*)?:lambda:[a-z]{2}((-gov)|(-iso(b?)))?-[a-z]+-\d{1}:\d{12}:code-signing-config:csc-[a-z0-9]{17}",  # noqa: E501
    )
    FunctionName: constr(
        min_length=1,
        max_length=140,
        pattern=r"(arn:(aws[a-zA-Z-]*)?:lambda:)?([a-z]{2}(-gov)?-[a-z]+-\d{1}:)?(\d{12}:)?(function:)?([a-zA-Z0-9-_]+)(:(\$LATEST|[a-zA-Z0-9-_]+))?",  # noqa: E501
    )
