from pydantic import BaseModel


class SelfManagedKafkaEventSourceConfig(BaseModel):
    """
    Specific configuration settings for a self-managed Apache Kafka event source.

    Attributes
    ----------
    ConsumerGroupId : Optional[str]
        The identifier for the Kafka consumer group to join. The consumer group ID
        must be unique among all your Kafka event sources.
        After creating a Kafka event source mapping with the consumer group ID
        specified, you cannot update this value.
    """

    ConsumerGroupId: str | None = None
