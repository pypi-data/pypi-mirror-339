from pydantic import BaseModel, conint, constr

from .data_types.dead_letter_config import DeadLetterConfig
from .data_types.environment import Environment
from .data_types.environment_response import EnvironmentResponse
from .data_types.ephemeral_storage import EphemeralStorage
from .data_types.file_system_config import FileSystemConfig
from .data_types.image_config import ImageConfig
from .data_types.image_config_response import ImageConfigResponse
from .data_types.layer import Layer
from .data_types.logging_config import LoggingConfig
from .data_types.runtime_version_config import RuntimeVersionConfig
from .data_types.snap_start import SnapStart
from .data_types.snap_start_response import SnapStartResponse
from .data_types.tracing_config import TracingConfig
from .data_types.tracing_config_response import TracingConfigResponse
from .data_types.vpc_config import VpcConfig
from .data_types.vpc_config_response import VpcConfigResponse


class UpdateFunctionConfigurationRequest(BaseModel):
    """
    Request model for updating the configuration of a Lambda function.

    Parameters
    ----------
    FunctionName : str
        The name or ARN of the Lambda function. The length constraint applies only to
        the full ARN. If you specify only the function name, it is limited to 64
        characters in length.
    DeadLetterConfig : Optional[DeadLetterConfig]
        A dead-letter queue configuration that specifies the queue or topic where Lambda
         sends asynchronous events when they fail processing.
    Description : Optional[str]
        A description of the function. Minimum length of 0. Maximum length of 256.
    Environment : Optional[Environment]
        Environment variables that are accessible from function code during execution.
    EphemeralStorage : Optional[EphemeralStorage]
        The size of the function's /tmp directory in MB.
    FileSystemConfigs : Optional[List[FileSystemConfig]]
        Connection settings for an Amazon EFS file system.
    Handler : Optional[str]
        The name of the method within your code that Lambda calls to run your function.
        Handler is required if the deployment package is a .zip file archive.
    ImageConfig : Optional[ImageConfig]
        Container image configuration values that override the values in the container
        image Docker file.
    KMSKeyArn : Optional[str]
        The ARN of the AWS Key Management Service (AWS KMS) customer managed key that's
        used to encrypt the function's environment variables and other resources.
    Layers : Optional[List[str]]
        A list of function layers to add to the function's execution environment.
        Specify each layer by its ARN, including the version.
    LoggingConfig : Optional[LoggingConfig]
        The function's Amazon CloudWatch Logs configuration settings.
    MemorySize : Optional[int]
        The amount of memory available to the function at runtime.
        Valid range: Minimum value of 128. Maximum value of 10240.
    RevisionId : Optional[str]
        Update the function only if the revision ID matches the ID that's specified.
    Role : Optional[str]
        The Amazon Resource Name (ARN) of the function's execution role.
    Runtime : Optional[str]
        The identifier of the function's runtime. Runtime is required if the deployment
        package is a .zip file archive.
    SnapStart : Optional[SnapStart]
        The function's SnapStart setting.
    Timeout : Optional[int]
        The amount of time (in seconds) that Lambda allows a function to run before
        stopping it. Valid range: Minimum value of 1. Maximum value of 900.
    TracingConfig : Optional[TracingConfig]
        Set Mode to Active to sample and trace a subset of incoming requests with X-Ray.
    VpcConfig : Optional[VpcConfig]
        For network connectivity to AWS resources in a VPC, specify a list of security
        groups and subnets in the VPC.
    """

    FunctionName: constr(
        min_length=1,
        max_length=140,
        pattern=r"(arn:(aws[a-zA-Z-]*)?:lambda:)?([a-z]{2}(-gov)?-[a-z]+-\d{1}:)?(\d{12}:)?(function:)?([a-zA-Z0-9-_]+)(:(\$LATEST|[a-zA-Z0-9-_]+))?",
    )  # noqa: E501
    DeadLetterConfig: DeadLetterConfig | None
    Description: constr(min_length=0, max_length=256) | None
    Environment: Environment | None
    EphemeralStorage: EphemeralStorage | None
    FileSystemConfigs: list[FileSystemConfig] | None
    Handler: constr(max_length=128, pattern=r"[^\s]+") | None
    ImageConfig: ImageConfig | None
    KMSKeyArn: constr(pattern=r"(arn:(aws[a-zA-Z-]*)?:[a-z0-9-.]+:.*)|()") | None
    Layers: (
        list[
            constr(
                min_length=1,
                max_length=140,
                pattern=r"arn:[a-zA-Z0-9-]+:lambda:[a-zA-Z0-9-]+:\d{12}:layer:[a-zA-Z0-9-_]+:[0-9]+",
            )
        ]
        | None
    )  # noqa: E501
    LoggingConfig: LoggingConfig | None
    MemorySize: conint(ge=128, le=10240) | None
    RevisionId: str | None
    Role: (
        constr(pattern=r"arn:(aws[a-zA-Z-]*)?:iam::\d{12}:role/?[a-zA-Z_0-9+=,.@\-_/]+")
        | None
    )  # noqa: E501
    Runtime: str | None
    SnapStart: SnapStart | None
    Timeout: conint(ge=1, le=900) | None
    TracingConfig: TracingConfig | None
    VpcConfig: VpcConfig | None


class UpdateFunctionConfigurationResponse(BaseModel):
    """
    Response model for updating the configuration of a Lambda function.
    """

    Architectures: list[str] | None
    CodeSha256: str | None
    CodeSize: int | None
    DeadLetterConfig: DeadLetterConfig | None
    Description: str | None
    Environment: EnvironmentResponse | None
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
    SnapStart: SnapStartResponse | None
    State: str | None
    StateReason: str | None
    StateReasonCode: str | None
    Timeout: int | None
    TracingConfig: TracingConfigResponse | None
    Version: str | None
    VpcConfig: VpcConfigResponse | None
