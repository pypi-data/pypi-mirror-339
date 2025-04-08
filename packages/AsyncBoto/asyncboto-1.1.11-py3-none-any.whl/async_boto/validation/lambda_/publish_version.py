from pydantic import BaseModel, constr

from .data_types.dead_letter_config import DeadLetterConfig
from .data_types.environment import Environment
from .data_types.ephemeral_storage import EphemeralStorage
from .data_types.file_system_config import FileSystemConfig
from .data_types.image_config_response import ImageConfigResponse
from .data_types.layer import Layer
from .data_types.logging_config import LoggingConfig
from .data_types.runtime_version_config import RuntimeVersionConfig
from .data_types.snap_start import SnapStart
from .data_types.tracing_config import TracingConfig
from .data_types.vpc_config import VpcConfig


class PublishVersionRequest(BaseModel):
    """
    Request model for publishing a new version of an AWS Lambda function.

    Attributes
    ----------
    FunctionName : str
        The name or ARN of the Lambda function.
    CodeSha256 : str
        Only publish a version if the hash value matches the value that's specified.
    Description : str
        A description for the version to override the description in the function
        configuration.
    RevisionId : str
        Only update the function if the revision ID matches the ID that's specified.
    """

    FunctionName: constr(
        min_length=1,
        max_length=140,
        pattern=r"(arn:(aws[a-zA-Z-]*)?:lambda:)?([a-z]{2}(-gov)?-[a-z]+-\d{1}:)?(\d{12}:)?(function:)?([a-zA-Z0-9-_]+)(:(\$LATEST|[a-zA-Z0-9-_]+))?",  # noqa: E501
    )
    CodeSha256: str | None
    Description: constr(max_length=256) | None
    RevisionId: str | None


class PublishVersionResponse(BaseModel):
    """
    Response model for publishing a new version of an AWS Lambda function.

    Attributes
    ----------
    Architectures : list
        The instruction set architecture that the function supports.
    CodeSha256 : str
        The SHA256 hash of the function's deployment package.
    CodeSize : int
        The size of the function's deployment package, in bytes.
    DeadLetterConfig : DeadLetterConfig
        The function's dead letter queue.
    Description : str
        The function's description.
    Environment : Environment
        The function's environment variables.
    EphemeralStorage : EphemeralStorage
        The size of the function's /tmp directory in MB.
    FileSystemConfigs : list
        Connection settings for an Amazon EFS file system.
    FunctionArn : str
        The function's Amazon Resource Name (ARN).
    FunctionName : str
        The name of the function.
    Handler : str
        The function that Lambda calls to begin running your function.
    ImageConfigResponse : ImageConfigResponse
        The function's image configuration values.
    KMSKeyArn : str
        The ARN of the AWS Key Management Service (AWS KMS) customer managed key.
    LastModified : str
        The date and time that the function was last updated.
    LastUpdateStatus : str
        The status of the last update that was performed on the function.
    LastUpdateStatusReason : str
        The reason for the last update that was performed on the function.
    LastUpdateStatusReasonCode : str
        The reason code for the last update that was performed on the function.
    Layers : list
        The function's layers.
    LoggingConfig : LoggingConfig
        The function's Amazon CloudWatch Logs configuration settings.
    MasterArn : str
        For Lambda@Edge functions, the ARN of the main function.
    MemorySize : int
        The amount of memory available to the function at runtime.
    PackageType : str
        The type of deployment package.
    RevisionId : str
        The latest updated revision of the function or alias.
    Role : str
        The function's execution role.
    Runtime : str
        The identifier of the function's runtime.
    RuntimeVersionConfig : RuntimeVersionConfig
        The ARN of the runtime and any errors that occurred.
    SigningJobArn : str
        The ARN of the signing job.
    SigningProfileVersionArn : str
        The ARN of the signing profile version.
    SnapStart : SnapStart
        The function's SnapStart configuration.
    State : str
        The current state of the function.
    StateReason : str
        The reason for the function's current state.
    StateReasonCode : str
        The reason code for the function's current state.
    Timeout : int
        The amount of time in seconds that Lambda allows a function to run
        before stopping it.
    TracingConfig : TracingConfig
        The function's AWS X-Ray tracing configuration.
    Version : str
        The version of the Lambda function.
    VpcConfig : VpcConfig
        The function's networking configuration.
    """

    Architectures: list[str] | None
    CodeSha256: str | None
    CodeSize: int | None
    DeadLetterConfig: DeadLetterConfig | None
    Description: str | None
    Environment: Environment | None
    EphemeralStorage: EphemeralStorage | None
    FileSystemConfigs: list[FileSystemConfig] | None
    FunctionArn: str | None
    FunctionName: str | None
    Handler: str | None
    ImageConfigResponse: ImageConfigResponse | None
    KMSKeyArn: str | None
    LastModified: str | None
    LastUpdateStatus: str | None
    LastUpdateStatusReason: str | None
    LastUpdateStatusReasonCode: str | None
    Layers: list[Layer] | None
    LoggingConfig: LoggingConfig | None
    MasterArn: str | None
    MemorySize: int | None
    PackageType: str | None
    RevisionId: str | None
    Role: str | None
    Runtime: str | None
    RuntimeVersionConfig: RuntimeVersionConfig | None
    SigningJobArn: str | None
    SigningProfileVersionArn: str | None
    SnapStart: SnapStart | None
    State: str | None
    StateReason: str | None
    StateReasonCode: str | None
    Timeout: int | None
    TracingConfig: TracingConfig | None
    Version: str | None
    VpcConfig: VpcConfig | None
