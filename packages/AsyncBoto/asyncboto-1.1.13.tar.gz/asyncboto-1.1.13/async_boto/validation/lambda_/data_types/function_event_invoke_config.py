from typing import Annotated

from pydantic import BaseModel, Field

from .destination_config import DestinationConfig as DestinationConfigModel


class FunctionEventInvokeConfig(BaseModel):
    """
    Configuration for asynchronous invocation of a Lambda function.

    Parameters
    ----------
    DestinationConfig : Optional[DestinationConfig], optional
        A destination for events after they have been sent to a function for processing.
    FunctionArn : Optional[str], optional
        The Amazon Resource Name (ARN) of the function.
    LastModified : Optional[float], optional
        The date and time that the configuration was last updated, in Unix time seconds.
    MaximumEventAgeInSeconds : Optional[int], optional
        The maximum age of a request that Lambda sends to a function for processing.
    MaximumRetryAttempts : Optional[int], optional
        The maximum number of times to retry when the function returns an error.
    """

    DestinationConfig: DestinationConfigModel | None = None
    FunctionArn: str | None = None
    LastModified: float | None = None
    MaximumEventAgeInSeconds: Annotated[int | None, Field(ge=60, le=21600)] = None
    MaximumRetryAttempts: Annotated[int | None, Field(ge=0, le=2)] = None
