from pydantic import BaseModel


class SelfManagedEventSource(BaseModel):
    """
    The self-managed Apache Kafka cluster for the event source.

    Attributes
    ----------
    Endpoints : Optional[Dict[str, List[str]]]
        The list of bootstrap servers for Kafka brokers.
        Typically uses the key 'KAFKA_BOOTSTRAP_SERVERS' with a list of broker
        endpoints.
        Each endpoint should be in the format 'hostname:port'.
    """

    Endpoints: dict[str, list[str]] | None = None
