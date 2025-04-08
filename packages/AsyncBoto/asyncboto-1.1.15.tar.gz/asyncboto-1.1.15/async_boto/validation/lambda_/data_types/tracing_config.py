from typing import Literal

from pydantic import BaseModel


class TracingConfig(BaseModel):
    """
    The function's AWS X-Ray tracing configuration.
    To sample and record incoming requests, set Mode to Active.

    Attributes
    ----------
    Mode : Optional[Literal["Active", "PassThrough"]]
        The tracing mode.
    """

    Mode: Literal["Active", "PassThrough"] | None = None
