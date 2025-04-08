from typing import Literal

from pydantic import BaseModel


class ScheduledQueryInsights(BaseModel):
    """
    Encapsulates settings for enabling `QueryInsights` on an
    `ExecuteScheduledQueryRequest`.

    Parameters
    ----------
    Mode : Literal['ENABLED_WITH_RATE_CONTROL', 'DISABLED']
        Provides the following modes to enable `ScheduledQueryInsights`:
        * `ENABLED_WITH_RATE_CONTROL` – Enables `ScheduledQueryInsights` for the
          queries being processed. This mode also includes a rate control mechanism,
          which limits the `QueryInsights` feature to 1 query per second (QPS).
        * `DISABLED` – Disables `ScheduledQueryInsights`.
    """

    Mode: Literal["ENABLED_WITH_RATE_CONTROL", "DISABLED"]
