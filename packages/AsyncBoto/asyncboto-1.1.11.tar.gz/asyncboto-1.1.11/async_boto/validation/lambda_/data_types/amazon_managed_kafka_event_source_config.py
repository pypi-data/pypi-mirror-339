from pydantic import BaseModel, Field


class AmazonManagedKafkaEventSourceConfig(BaseModel):
    r"""
    Specific configuration settings for an Amazon Managed Streaming for Apache Kafka
    (Amazon MSK) event source.

    This configuration allows customizing how Lambda connects to and processes records
    from Amazon MSK clusters.

    Parameters
    ----------
    ConsumerGroupId : Optional[str]
        The identifier for the Kafka consumer group to join.
        The consumer group ID must be unique among all your Kafka event sources.
        After creating a Kafka event source mapping with the consumer group ID
        specified, you cannot update this value.

        This allows for better control over how Lambda consumes records from Kafka
        topics,
        including the ability to coordinate with other Kafka consumers (both Lambda and
        non-Lambda).

        When not specified, Lambda generates a unique consumer group ID for the event
        source mapping.

        Constraints:
          - Min length: 1
          - Max length: 200
          - Pattern: [a-zA-Z0-9-\/*:_+=.@-]*
    """

    ConsumerGroupId: str | None = Field(
        None, min_length=1, max_length=200, pattern=r"[a-zA-Z0-9-\/*:_+=.@-]*"
    )
