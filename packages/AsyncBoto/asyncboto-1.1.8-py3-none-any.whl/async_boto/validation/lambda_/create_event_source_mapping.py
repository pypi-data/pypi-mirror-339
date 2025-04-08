# ruff: noqa: E501
from pydantic import BaseModel

from .data_types.amazon_managed_kafka_event_source_config import (
    AmazonManagedKafkaEventSourceConfig as AmazonManagedKafkaEventSourceConfigModel,
)
from .data_types.destination_config import DestinationConfig as DestinationConfigModel
from .data_types.document_db_event_source_config import (
    DocumentDBEventSourceConfig as DocumentDBEventSourceConfigModel,
)
from .data_types.filter_criteria import FilterCriteria as FilterCriteriaModel
from .data_types.filter_criteria_error import (
    FilterCriteriaError as FilterCriteriaErrorModel,
)
from .data_types.provisioned_poller_config import (
    ProvisionedPollerConfig as ProvisionedPollerConfigModel,
)
from .data_types.scaling_config import ScalingConfig as ScalingConfigModel
from .data_types.self_managed_event_source import (
    SelfManagedEventSource as SelfManagedEventSourceModel,
)
from .data_types.self_managed_kafka_event_source_config import (
    SelfManagedKafkaEventSourceConfig as SelfManagedKafkaEventSourceConfigModel,
)
from .data_types.source_access_configuration import (
    SourceAccessConfiguration as SourceAccessConfigurationModel,
)


class CreateEventSourceMappingRequest(BaseModel):
    """
    Request model for creating an event source mapping.

    Parameters
    ----------
    AmazonManagedKafkaEventSourceConfig : AmazonManagedKafkaEventSourceConfig, optional
        Specific configuration settings for an Amazon Managed Streaming for Apache Kafka (Amazon MSK) event source.
    BatchSize : int, optional
        The maximum number of records in each batch that Lambda pulls from your stream or queue and sends to your function.
    BisectBatchOnFunctionError : bool, optional
        If the function returns an error, split the batch in two and retry.
    DestinationConfig : DestinationConfig, optional
        A configuration object that specifies the destination of an event after Lambda processes it.
    DocumentDBEventSourceConfig : DocumentDBEventSourceConfig, optional
        Specific configuration settings for a DocumentDB event source.
    Enabled : bool, optional
        When true, the event source mapping is active. When false, Lambda pauses polling and invocation.
    EventSourceArn : str, optional
        The Amazon Resource Name (ARN) of the event source.
    FilterCriteria : FilterCriteria, optional
        An object that defines the filter criteria that determine whether Lambda should process an event.
    FunctionName : str
        The name or ARN of the Lambda function.
    FunctionResponseTypes : List[str], optional
        A list of current response type enums applied to the event source mapping.
    KMSKeyArn : str, optional
        The ARN of the AWS Key Management Service (AWS KMS) customer managed key that Lambda uses to encrypt your function's filter criteria.
    MaximumBatchingWindowInSeconds : int, optional
        The maximum amount of time, in seconds, that Lambda spends gathering records before invoking the function.
    MaximumRecordAgeInSeconds : int, optional
        Discard records older than the specified age.
    MaximumRetryAttempts : int, optional
        Discard records after the specified number of retries.
    MetricsConfig : Dict, optional
        The metrics configuration for your event source.
    ParallelizationFactor : int, optional
        The number of batches to process from each shard concurrently.
    ProvisionedPollerConfig : ProvisionedPollerConfig, optional
        The provisioned mode configuration for the event source.
    Queues : List[str], optional
        The name of the Amazon MQ broker destination queue to consume.
    ScalingConfig : ScalingConfig, optional
        The scaling configuration for the event source.
    SelfManagedEventSource : SelfManagedEventSource, optional
        The self-managed Apache Kafka cluster to receive records from.
    SelfManagedKafkaEventSourceConfig : SelfManagedKafkaEventSourceConfig, optional
        Specific configuration settings for a self-managed Apache Kafka event source.
    SourceAccessConfigurations : List[SourceAccessConfiguration], optional
        An array of authentication protocols or VPC components required to secure your event source.
    StartingPosition : str, optional
        The position in a stream from which to start reading.
    StartingPositionTimestamp : float, optional
        With StartingPosition set to AT_TIMESTAMP, the time from which to start reading, in Unix time seconds.
    Tags : Dict[str, str], optional
        A list of tags to apply to the event source mapping.
    Topics : List[str], optional
        The name of the Kafka topic.
    TumblingWindowInSeconds : int, optional
        The duration in seconds of a processing window for DynamoDB and Kinesis Streams event sources.
    """

    FunctionName: str
    AmazonManagedKafkaEventSourceConfig: (
        AmazonManagedKafkaEventSourceConfigModel | None
    ) = None
    BatchSize: int | None = None
    BisectBatchOnFunctionError: bool | None = None
    DestinationConfig: DestinationConfigModel | None = None
    DocumentDBEventSourceConfig: DocumentDBEventSourceConfigModel | None = None
    Enabled: bool | None = None
    EventSourceArn: str | None = None
    FilterCriteria: FilterCriteriaModel | None = None
    FunctionResponseTypes: list[str] | None = None
    KMSKeyArn: str | None = None
    MaximumBatchingWindowInSeconds: int | None = None
    MaximumRecordAgeInSeconds: int | None = None
    MaximumRetryAttempts: int | None = None
    MetricsConfig: dict | None = None
    ParallelizationFactor: int | None = None
    ProvisionedPollerConfig: ProvisionedPollerConfigModel | None = None
    Queues: list[str] | None = None
    ScalingConfig: ScalingConfigModel | None = None
    SelfManagedEventSource: SelfManagedEventSourceModel | None = None
    SelfManagedKafkaEventSourceConfig: SelfManagedKafkaEventSourceConfigModel | None = (
        None
    )
    SourceAccessConfigurations: list[SourceAccessConfigurationModel] | None = None
    StartingPosition: str | None = None
    StartingPositionTimestamp: float | None = None
    Tags: dict[str, str] | None = None
    Topics: list[str] | None = None
    TumblingWindowInSeconds: int | None = None


class CreateEventSourceMappingResponse(BaseModel):
    """
    Response model for creating an event source mapping.

    Parameters
    ----------
    AmazonManagedKafkaEventSourceConfig : AmazonManagedKafkaEventSourceConfig, optional
        Specific configuration settings for an Amazon MSK event source.
    BatchSize : int, optional
        The maximum number of records in each batch that Lambda pulls from your stream or queue.
    BisectBatchOnFunctionError : bool, optional
        If the function returns an error, split the batch in two and retry.
    DestinationConfig : DestinationConfig, optional
        A configuration object that specifies the destination of an event after Lambda processes it.
    DocumentDBEventSourceConfig : DocumentDBEventSourceConfig, optional
        Specific configuration settings for a DocumentDB event source.
    EventSourceArn : str, optional
        The Amazon Resource Name (ARN) of the event source.
    EventSourceMappingArn : str, optional
        The Amazon Resource Name (ARN) of the event source mapping.
    FilterCriteria : FilterCriteria, optional
        An object that defines the filter criteria that determine whether Lambda should process an event.
    FilterCriteriaError : FilterCriteriaError, optional
        An object that contains details about an error related to filter criteria encryption.
    FunctionArn : str, optional
        The ARN of the Lambda function.
    FunctionResponseTypes : List[str], optional
        A list of current response type enums applied to the event source mapping.
    KMSKeyArn : str, optional
        The ARN of the AWS KMS key that Lambda uses to encrypt your function's filter criteria.
    LastModified : float, optional
        The date that the event source mapping was last updated, in Unix time seconds.
    LastProcessingResult : str, optional
        The result of the last Lambda invocation of your function.
    MaximumBatchingWindowInSeconds : int, optional
        The maximum amount of time, in seconds, that Lambda spends gathering records before invoking the function.
    MaximumRecordAgeInSeconds : int, optional
        Discard records older than the specified age.
    MaximumRetryAttempts : int, optional
        Discard records after the specified number of retries.
    MetricsConfig : Dict, optional
        The metrics configuration for your event source.
    ParallelizationFactor : int, optional
        The number of batches to process concurrently from each shard.
    ProvisionedPollerConfig : ProvisionedPollerConfig, optional
        The provisioned mode configuration for the event source.
    Queues : List[str], optional
        The name of the Amazon MQ broker destination queue to consume.
    ScalingConfig : ScalingConfig, optional
        The scaling configuration for the event source.
    SelfManagedEventSource : SelfManagedEventSource, optional
        The self-managed Apache Kafka cluster for your event source.
    SelfManagedKafkaEventSourceConfig : SelfManagedKafkaEventSourceConfig, optional
        Specific configuration settings for a self-managed Apache Kafka event source.
    SourceAccessConfigurations : List[SourceAccessConfiguration], optional
        An array of authentication protocols, VPC components, or virtual host for your event source.
    StartingPosition : str, optional
        The position in a stream from which to start reading.
    StartingPositionTimestamp : float, optional
        With StartingPosition set to AT_TIMESTAMP, the time from which to start reading.
    State : str, optional
        The state of the event source mapping.
    StateTransitionReason : str, optional
        Indicates whether a user or Lambda made the last change to the event source mapping.
    Topics : List[str], optional
        The name of the Kafka topic.
    TumblingWindowInSeconds : int, optional
        The duration in seconds of a processing window for DynamoDB and Kinesis Streams event sources.
    UUID : str, optional
        The identifier of the event source mapping.
    """

    AmazonManagedKafkaEventSourceConfig: (
        AmazonManagedKafkaEventSourceConfigModel | None
    ) = None
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
    LastModified: float | None = None
    LastProcessingResult: str | None = None
    MaximumBatchingWindowInSeconds: int | None = None
    MaximumRecordAgeInSeconds: int | None = None
    MaximumRetryAttempts: int | None = None
    MetricsConfig: dict | None = None
    ParallelizationFactor: int | None = None
    ProvisionedPollerConfig: ProvisionedPollerConfigModel | None = None
    Queues: list[str] | None = None
    ScalingConfig: ScalingConfigModel | None = None
    SelfManagedEventSource: SelfManagedEventSourceModel | None = None
    SelfManagedKafkaEventSourceConfig: SelfManagedKafkaEventSourceConfigModel | None = (
        None
    )
    SourceAccessConfigurations: list[SourceAccessConfigurationModel] | None = None
    StartingPosition: str | None = None
    StartingPositionTimestamp: float | None = None
    State: str | None = None
    StateTransitionReason: str | None = None
    Topics: list[str] | None = None
    TumblingWindowInSeconds: int | None = None
    UUID: str | None = None
