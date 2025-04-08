from pydantic import BaseModel, constr

from .data_types.amazon_managed_kafka_event_source_config import (
    AmazonManagedKafkaEventSourceConfig,
)
from .data_types.destination_config import DestinationConfig
from .data_types.document_db_event_source_config import DocumentDBEventSourceConfig
from .data_types.event_source_mapping_metrics_config import (
    EventSourceMappingMetricsConfig,
)
from .data_types.filter_criteria import FilterCriteria
from .data_types.filter_criteria_error import FilterCriteriaError
from .data_types.provisioned_poller_config import ProvisionedPollerConfig
from .data_types.scaling_config import ScalingConfig
from .data_types.self_managed_event_source import SelfManagedEventSource
from .data_types.self_managed_kafka_event_source_config import (
    SelfManagedKafkaEventSourceConfig,
)
from .data_types.source_access_configuration import SourceAccessConfiguration


class GetEventSourceMappingRequest(BaseModel):
    """
    Request model for retrieving details about an event source mapping.

    Attributes
    ----------
    UUID : str
        The identifier of the event source mapping.
    """

    UUID: constr(min_length=1)


class GetEventSourceMappingResponse(BaseModel):
    AmazonManagedKafkaEventSourceConfig: AmazonManagedKafkaEventSourceConfig | None
    BatchSize: int | None
    BisectBatchOnFunctionError: bool | None
    DestinationConfig: DestinationConfig | None
    DocumentDBEventSourceConfig: DocumentDBEventSourceConfig | None
    EventSourceArn: str | None
    EventSourceMappingArn: str | None
    FilterCriteria: FilterCriteria | None
    FilterCriteriaError: FilterCriteriaError | None
    FunctionArn: str | None
    FunctionResponseTypes: list[str] | None
    KMSKeyArn: str | None
    LastModified: int | None
    LastProcessingResult: str | None
    MaximumBatchingWindowInSeconds: int | None
    MaximumRecordAgeInSeconds: int | None
    MaximumRetryAttempts: int | None
    MetricsConfig: EventSourceMappingMetricsConfig | None
    ParallelizationFactor: int | None
    ProvisionedPollerConfig: ProvisionedPollerConfig | None
    Queues: list[str] | None
    ScalingConfig: ScalingConfig | None
    SelfManagedEventSource: SelfManagedEventSource | None
    SelfManagedKafkaEventSourceConfig: SelfManagedKafkaEventSourceConfig | None
    SourceAccessConfigurations: list[SourceAccessConfiguration] | None
    StartingPosition: str | None
    StartingPositionTimestamp: int | None
    State: str | None
    StateTransitionReason: str | None
    Topics: list[str] | None
    TumblingWindowInSeconds: int | None
    UUID: str | None
