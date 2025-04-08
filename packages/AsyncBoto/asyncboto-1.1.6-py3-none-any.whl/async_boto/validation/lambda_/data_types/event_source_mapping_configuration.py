from datetime import datetime

from pydantic import BaseModel

# Import related models
from .amazon_managed_kafka_event_source_config import (
    AmazonManagedKafkaEventSourceConfig as AmazonManagedKafkaEventSourceConfigModel,
)
from .destination_config import DestinationConfig as DestinationConfigModel
from .document_db_event_source_config import (
    DocumentDBEventSourceConfig as DocumentDBEventSourceConfigModel,
)
from .event_source_mapping_metrics_config import EventSourceMappingMetricsConfig
from .filter_criteria import FilterCriteria as FilterCriteriaModel
from .filter_criteria_error import FilterCriteriaError as FilterCriteriaErrorModel
from .provisioned_poller_config import (
    ProvisionedPollerConfig as ProvisionedPollerConfigModel,
)
from .scaling_config import ScalingConfig as ScalingConfigModel
from .self_managed_event_source import (
    SelfManagedEventSource as SelfManagedEventSourceModel,
)
from .self_managed_kafka_event_source_config import (
    SelfManagedKafkaEventSourceConfig as SelfManagedKafkaEventSourceConfigModel,
)
from .source_access_configuration import SourceAccessConfiguration


class EventSourceMappingConfiguration(BaseModel):
    """
    A mapping between an AWS resource and a Lambda function.

    Parameters
    ----------
    AmazonManagedKafkaEventSourceConfig : Optional[AmazonManagedKafkaEventSourceConfig]
        Specific configuration settings for an Amazon Managed Streaming for Apache
        Kafka event source.
    BatchSize : Optional[int]
        The maximum number of records in each batch.
    BisectBatchOnFunctionError : Optional[bool]
        For Kinesis and DynamoDB Streams only, when true, splits the batch in two and
        retries if function returns an error.
    DestinationConfig : Optional[DestinationConfig]
        A configuration object that specifies the destination of an event after Lambda
        processes it.
    DocumentDBEventSourceConfig : Optional[DocumentDBEventSourceConfig]
        Specific configuration settings for a DocumentDB event source.
    EventSourceArn : Optional[str]
        The Amazon Resource Name (ARN) of the event source.
    EventSourceMappingArn : Optional[str]
        The Amazon Resource Name (ARN) of the event source mapping.
    FilterCriteria : Optional[FilterCriteria]
        Object that defines filter criteria for determining whether Lambda should
        process an event.
    FilterCriteriaError : Optional[FilterCriteriaError]
        Object that contains details about an error related to filter criteria
        encryption.
    FunctionArn : Optional[str]
        The ARN of the Lambda function.
    FunctionResponseTypes : Optional[List[str]]
        A list of current response type enums applied to the event source mapping.
    KMSKeyArn : Optional[str]
        The ARN of the AWS KMS customer managed key used to encrypt filter criteria.
    LastModified : Optional[datetime]
        The date that the event source mapping was last updated or state changed.
    LastProcessingResult : Optional[str]
        The result of the last Lambda invocation of your function.
    MaximumBatchingWindowInSeconds : Optional[int]
        The maximum amount of time to gather records before invoking the function.
    MaximumRecordAgeInSeconds : Optional[int]
        For Kinesis and DynamoDB Streams only, discard records older than specified age.
    MaximumRetryAttempts : Optional[int]
        For Kinesis and DynamoDB Streams only, discard records after specified number
        of retries.
    MetricsConfig : Optional[EventSourceMappingMetricsConfig]
        The metrics configuration for your event source.
    ParallelizationFactor : Optional[int]
        For Kinesis and DynamoDB Streams only, number of batches to process concurrently
         from each shard.
    ProvisionedPollerConfig : Optional[ProvisionedPollerConfig]
        For Amazon MSK and self-managed Apache Kafka, provisioned mode configuration
        for the event source.
    Queues : Optional[List[str]]
        For Amazon MQ, the name of the broker destination queue to consume.
    ScalingConfig : Optional[ScalingConfig]
        For Amazon SQS only, the scaling configuration for the event source.
    SelfManagedEventSource : Optional[SelfManagedEventSource]
        The self-managed Apache Kafka cluster for your event source.
    SelfManagedKafkaEventSourceConfig : Optional[SelfManagedKafkaEventSourceConfig]
        Specific configuration settings for a self-managed Apache Kafka event source.
    SourceAccessConfigurations : Optional[List[SourceAccessConfiguration]]
        Array of authentication protocol, VPC components, or virtual host for the event
        source.
    StartingPosition : Optional[str]
        The position in a stream from which to start reading.
    StartingPositionTimestamp : Optional[datetime]
        With StartingPosition set to AT_TIMESTAMP, the time from which to start reading.
    State : Optional[str]
        The state of the event source mapping.
    StateTransitionReason : Optional[str]
        Indicates whether a user or Lambda made the last change to the event source
        mapping.
    Topics : Optional[List[str]]
        The name of the Kafka topic.
    TumblingWindowInSeconds : Optional[int]
        For Kinesis and DynamoDB Streams only, the duration in seconds of a processing
        window.
    UUID : Optional[str]
        The identifier of the event source mapping.
    """

    AmazonManagedKafkaEventSourceConfig: (
        AmazonManagedKafkaEventSourceConfigModel | None
    ) = (  # noqa: E501
        None
    )
    BatchSize: int | None = None
    BisectBatchOnFunctionError: bool | None = None
    DestinationConfig: DestinationConfigModel | None = None
    DocumentDBEventSourceConfig: DocumentDBEventSourceConfigModel | None = None
    EventSourceArn: str | None = None
    EventSourceMappingArn: str | None = None
    FilterCriteria: FilterCriteriaModel | None = None
    FilterCriteriaError: FilterCriteriaErrorModel | None = None
    FunctionArn: str | None = None
    FunctionResponseTypes: list[str] | None = None
    KMSKeyArn: str | None = None
    LastModified: datetime | None = None
    LastProcessingResult: str | None = None
    MaximumBatchingWindowInSeconds: int | None = None
    MaximumRecordAgeInSeconds: int | None = None
    MaximumRetryAttempts: int | None = None
    MetricsConfig: EventSourceMappingMetricsConfig | None = None
    ParallelizationFactor: int | None = None
    ProvisionedPollerConfig: ProvisionedPollerConfigModel | None = None
    Queues: list[str] | None = None
    ScalingConfig: ScalingConfigModel | None = None
    SelfManagedEventSource: SelfManagedEventSourceModel | None = None
    SelfManagedKafkaEventSourceConfig: SelfManagedKafkaEventSourceConfigModel | None = (
        None  # noqa: E501
    )
    SourceAccessConfigurations: list[SourceAccessConfiguration] | None = None
    StartingPosition: str | None = None
    StartingPositionTimestamp: datetime | None = None
    State: str | None = None
    StateTransitionReason: str | None = None
    Topics: list[str] | None = None
    TumblingWindowInSeconds: int | None = None
    UUID: str | None = None
