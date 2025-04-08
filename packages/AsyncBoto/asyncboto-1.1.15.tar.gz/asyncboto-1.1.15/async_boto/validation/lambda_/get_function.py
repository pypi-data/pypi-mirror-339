from pydantic import BaseModel, constr

from .data_types.concurrency import Concurrency
from .data_types.function_code_location import FunctionCodeLocation
from .data_types.function_configuration import FunctionConfiguration
from .data_types.tags_error import TagsError


class GetFunctionRequest(BaseModel):
    """
    Request model for retrieving information about a Lambda function or function
    version.

    Attributes
    ----------
    FunctionName : str
        The name or ARN of the Lambda function, version, or alias.
    Qualifier : str
        Specify a version or alias to get details about a published version of the
        function.
    """

    FunctionName: constr(
        min_length=1,
        max_length=170,
        pattern=r"(arn:(aws[a-zA-Z-]*)?:lambda:)?([a-z]{2}(-gov)?-[a-z]+-\d{1}:)?(\d{12}:)?(function:)?([a-zA-Z0-9-_\.]+)(:(\$LATEST|[a-zA-Z0-9-_]+))?",  # noqa: E501
    )
    Qualifier: constr(min_length=1, max_length=128, pattern=r"(|[a-zA-Z0-9$_-]+)")


class GetFunctionResponse(BaseModel):
    Code: FunctionCodeLocation | None
    Concurrency: Concurrency | None
    Configuration: FunctionConfiguration | None
    Tags: dict[str, str] | None
    TagsError: TagsError | None
