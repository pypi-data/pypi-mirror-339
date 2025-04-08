from pydantic import BaseModel, conint, constr

from .data_types.destination_config import DestinationConfig
from .data_types.document_db_event_source_config import DocumentDBEventSourceConfig
from .data_types.event_source_mapping_metrics_config import (
    EventSourceMappingMetricsConfig,
)
from .data_types.filter_criteria import FilterCriteria
from .data_types.filter_criteria_error import FilterCriteriaError
from .data_types.provisioned_poller_config import ProvisionedPollerConfig
from .data_types.scaling_config import ScalingConfig
from .data_types.source_access_configuration import SourceAccessConfiguration


class UpdateEventSourceMappingRequest(BaseModel):
    UUID: constr(min_length=1, max_length=256)
    BatchSize: conint(ge=1, le=10000) | None
    BisectBatchOnFunctionError: bool | None
    DestinationConfig: DestinationConfig | None
    DocumentDBEventSourceConfig: DocumentDBEventSourceConfig | None
    Enabled: bool | None
    FilterCriteria: FilterCriteria | None
    FunctionName: (
        constr(
            min_length=1,
            max_length=140,
            pattern=r"(arn:(aws[a-zA-Z-]*)?:lambda:)?([a-z]{2}(-gov)?-[a-z]+-\d{1}:)?(\d{12}:)?(function:)?([a-zA-Z0-9-_]+)(:(\$LATEST|[a-zA-Z0-9-_]+))?",  # noqa: E501
        )
        | None
    )
    FunctionResponseTypes: list[str] | None
    KMSKeyArn: constr(pattern=r"(arn:(aws[a-zA-Z-]*)?:[a-z0-9-.]+:.*)|()") | None
    MaximumBatchingWindowInSeconds: conint(ge=0, le=300) | None
    MaximumRecordAgeInSeconds: conint(ge=-1, le=604800) | None
    MaximumRetryAttempts: conint(ge=-1, le=10000) | None
    MetricsConfig: EventSourceMappingMetricsConfig | None
    ParallelizationFactor: conint(ge=1, le=10) | None
    ProvisionedPollerConfig: ProvisionedPollerConfig | None
    ScalingConfig: ScalingConfig | None
    SourceAccessConfigurations: list[SourceAccessConfiguration] | None
    TumblingWindowInSeconds: conint(ge=0, le=900) | None


class UpdateEventSourceMappingResponse(BaseModel):
    AmazonManagedKafkaEventSourceConfig: dict[str, str] | None
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
    SelfManagedEventSource: dict[str, list[str]] | None
    SelfManagedKafkaEventSourceConfig: dict[str, str] | None
    SourceAccessConfigurations: list[SourceAccessConfiguration] | None
    StartingPosition: str | None
    StartingPositionTimestamp: int | None
    State: str | None
    StateTransitionReason: str | None
    Topics: list[str] | None
    TumblingWindowInSeconds: int | None
    UUID: str | None
