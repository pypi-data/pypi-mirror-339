from pydantic import BaseModel

from .sns_configuration import SnsConfiguration


class NotificationConfiguration(BaseModel):
    """
    Notification configuration for a scheduled query. A notification is sent by
    Timestream
    when a scheduled query is created, its state is updated or when it is deleted.

    Parameters
    ----------
    SnsConfiguration : SnsConfiguration
        Details about the Amazon Simple Notification Service (SNS) configuration.
        This field is visible only when SNS Topic is provided when updating the
        account settings.
    """

    SnsConfiguration: SnsConfiguration
