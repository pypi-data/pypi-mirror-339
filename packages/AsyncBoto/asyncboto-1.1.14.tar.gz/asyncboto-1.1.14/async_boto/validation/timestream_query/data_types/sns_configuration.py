from pydantic import BaseModel, Field


class SnsConfiguration(BaseModel):
    """
    Details on SNS that are required to send the notification.

    Parameters
    ----------
    TopicArn : str
        SNS topic ARN that the scheduled query status notifications will be sent to.
    """

    TopicArn: str = Field(min_length=1, max_length=2048)
