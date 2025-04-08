from pydantic import BaseModel, Field


class Concurrency(BaseModel):
    """
    Represents reserved concurrency settings for a Lambda function.

    Concurrency is the number of simultaneous executions that can be allocated
    to a function at a given time. By reserving concurrency, you guarantee
    that a function can always reach a specified level of concurrency.

    Parameters
    ----------
    ReservedConcurrentExecutions : Optional[int]
        The number of concurrent executions that are reserved for this function.

        This value is subtracted from your account's unreserved concurrency limit.
        Functions without reserved concurrency share the remaining pool.

        Setting this to 0 prevents the function from executing.
        Setting this value reserves the specified number of concurrent executions
        exclusively for this function.

        Minimum value: 0
    """

    ReservedConcurrentExecutions: int | None = Field(None, ge=0)
