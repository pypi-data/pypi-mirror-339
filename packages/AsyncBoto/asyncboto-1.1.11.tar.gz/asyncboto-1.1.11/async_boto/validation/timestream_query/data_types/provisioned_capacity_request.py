from pydantic import BaseModel

from .account_settings_notification_configuration import (
    AccountSettingsNotificationConfiguration,
)


class ProvisionedCapacityRequest(BaseModel):
    """
    A request to update the provisioned capacity settings for querying data.

    Parameters
    ----------
    TargetQueryTCU : int
        The target compute capacity for querying data, specified in Timestream
        Compute Units (TCUs).
    NotificationConfiguration : Optional[AccountSettingsNotificationConfiguration]
        Configuration settings for notifications related to the provisioned
        capacity update.
    """

    TargetQueryTCU: int
    NotificationConfiguration: AccountSettingsNotificationConfiguration | None = None
