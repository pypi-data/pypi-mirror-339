# ruff: noqa: E501
from typing import Literal

from pydantic import BaseModel


class LoggingConfig(BaseModel):
    """
    The function's Amazon CloudWatch Logs configuration settings.

    Attributes
    ----------
    ApplicationLogLevel : Optional[Literal['TRACE', 'DEBUG', 'INFO', 'WARN', 'ERROR', 'FATAL']]
        Set this property to filter the application logs for your function that Lambda
        sends to CloudWatch.
    LogFormat : Optional[Literal['JSON', 'Text']]
        The format in which Lambda sends your function's application and system logs to
        CloudWatch.
    LogGroup : Optional[str]
        The name of the Amazon CloudWatch log group the function sends logs to.
    SystemLogLevel : Optional[Literal['DEBUG', 'INFO', 'WARN']]
        Set this property to filter the system logs for your function that Lambda sends
        to CloudWatch.
    """

    ApplicationLogLevel: (
        Literal["TRACE", "DEBUG", "INFO", "WARN", "ERROR", "FATAL"] | None
    ) = None
    LogFormat: Literal["JSON", "Text"] | None = None
    LogGroup: str | None = None
    SystemLogLevel: Literal["DEBUG", "INFO", "WARN"] | None = None
