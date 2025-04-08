from typing import Literal

from pydantic import BaseModel


class TracingConfigResponse(BaseModel):
    """
    The function's AWS X-Ray tracing configuration.

    Attributes
    ----------
    Mode : Optional[Literal["Active", "PassThrough"]]
        The tracing mode.
    """

    Mode: Literal["Active", "PassThrough"] | None = None
