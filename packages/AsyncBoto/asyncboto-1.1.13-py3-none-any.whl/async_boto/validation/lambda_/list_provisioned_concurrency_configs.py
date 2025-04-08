from pydantic import BaseModel, constr

from .data_types.provisioned_concurrency_config_list_item import (
    ProvisionedConcurrencyConfigListItem,
)


class ListProvisionedConcurrencyConfigsRequest(BaseModel):
    """
    Request model for listing provisioned concurrency configurations.

    Attributes
    ----------
    FunctionName : str
        The name or ARN of the Lambda function.
    Marker : str
        Specify the pagination token that's returned by a previous request to retrieve
        the next page of results.
    MaxItems : int
        Specify a number to limit the number of configurations returned.
    """

    FunctionName: constr(
        min_length=1,
        max_length=140,
        pattern=r"(arn:(aws[a-zA-Z-]*)?:lambda:)?([a-z]{2}(-gov)?-[a-z]+-\d{1}:)?(\d{12}:)?(function:)?([a-zA-Z0-9-_]+)(:(\$LATEST|[a-zA-Z0-9-_]+))?",  # noqa: E501
    )
    Marker: str | None
    MaxItems: int | None


class ListProvisionedConcurrencyConfigsResponse(BaseModel):
    """
    Response model for listing provisioned concurrency configurations.

    Attributes
    ----------
    NextMarker : str
        The pagination token that's included if more results are available.
    ProvisionedConcurrencyConfigs : list
        A list of provisioned concurrency configurations.
    """

    NextMarker: str | None
    ProvisionedConcurrencyConfigs: list[ProvisionedConcurrencyConfigListItem]
