from pydantic import BaseModel, constr

from .sns_configuration import SnsConfiguration


class AccountSettingsNotificationConfiguration(BaseModel):
    """
    Configuration settings for notifications related to account settings.

    Attributes
    ----------
    RoleArn : constr
        An Amazon Resource Name (ARN) that grants Timestream permission to publish
        notifications. This field is only visible if SNS Topic is provided when
        updating the account settings.
    SnsConfiguration : Optional[SnsConfiguration]
        Details on SNS that are required to send the notification.
    """

    RoleArn: constr(min_length=1, max_length=2048)
    SnsConfiguration: SnsConfiguration | None = None
