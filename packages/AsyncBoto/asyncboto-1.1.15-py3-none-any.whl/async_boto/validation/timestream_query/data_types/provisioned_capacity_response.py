from pydantic import BaseModel

from .account_settings_notification_configuration import (
    AccountSettingsNotificationConfiguration,
)
from .last_update import LastUpdate


class ProvisionedCapacityResponse(BaseModel):
    """
    The response to a request to update the provisioned capacity settings for
    querying data.

    Parameters
    ----------
    ActiveQueryTCU : Optional[int]
        The number of Timestream Compute Units (TCUs) provisioned in the account.
        This field is only visible when the compute mode is `PROVISIONED`.
    LastUpdate : Optional[LastUpdate]
        Information about the last update to the provisioned capacity settings.
    NotificationConfiguration : Optional[AccountSettingsNotificationConfiguration]
        An object that contains settings for notifications that are sent whenever the
        provisioned capacity settings are modified. This field is only visible when
        the compute mode is `PROVISIONED`.
    """

    ActiveQueryTCU: int | None = None
    LastUpdate: LastUpdate | None = None
    NotificationConfiguration: AccountSettingsNotificationConfiguration | None = None
