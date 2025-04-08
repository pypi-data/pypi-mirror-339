from pydantic import BaseModel


class ScalingConfig(BaseModel):
    """
    Scaling configuration for an Amazon SQS event source.

    Attributes
    ----------
    MaximumConcurrency : Optional[int]
        Limits the number of concurrent instances that the Amazon SQS
        event source can invoke.
    """

    MaximumConcurrency: int | None = None
