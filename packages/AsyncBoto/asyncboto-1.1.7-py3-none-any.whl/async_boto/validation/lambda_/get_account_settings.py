from pydantic import BaseModel

from .data_types.account_limit import AccountLimit as AccountLimitModel
from .data_types.account_usage import AccountUsage as AccountUsageModel


class GetAccountSettingsRequest(BaseModel):
    """
    Request model for retrieving account settings.
    """

    pass


class GetAccountSettingsResponse(BaseModel):
    """
    Response model for retrieving account settings.

    Attributes
    ----------
    AccountLimit : AccountLimit
        Limits that are related to concurrency and code storage.
    AccountUsage : AccountUsage
        The number of functions and amount of storage in use.
    """

    AccountLimit: AccountLimitModel
    AccountUsage: AccountUsageModel
