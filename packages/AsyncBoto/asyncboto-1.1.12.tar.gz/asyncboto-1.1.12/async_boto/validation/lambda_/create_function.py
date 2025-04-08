from pydantic import BaseModel

from .data_types.dead_letter_config import DeadLetterConfig as DeadLetterConfigModel
from .data_types.environment import Environment as EnvironmentModel
from .data_types.environment_response import EnvironmentResponse
from .data_types.ephemeral_storage import EphemeralStorage as EphemeralStorageModel
from .data_types.file_system_config import FileSystemConfig
from .data_types.function_code import FunctionCode
from .data_types.image_config import ImageConfig as ImageConfigModel
from .data_types.image_config_response import (
    ImageConfigResponse as ImageConfigResponseModel,
)
from .data_types.layer import Layer
from .data_types.logging_config import LoggingConfig as LoggingConfigModel
from .data_types.runtime_version_config import (
    RuntimeVersionConfig as RuntimeVersionConfigModel,
)
from .data_types.snap_start import SnapStart as SnapStartModel
from .data_types.snap_start_response import SnapStartResponse
from .data_types.tracing_config import TracingConfig as TracingConfigModel
from .data_types.tracing_config_response import TracingConfigResponse
from .data_types.vpc_config import VpcConfig as VpcConfigModel
from .data_types.vpc_config_response import VpcConfigResponse


class CreateFunctionRequest(BaseModel):
    """
    Request model for creating a Lambda function.

    Parameters
    ----------
    Architectures : List[str], optional
        The instruction set architecture that the function supports.
    Code : FunctionCode
        The code for the function.
    CodeSigningConfigArn : str, optional
        To enable code signing for this function, specify the ARN of a code-signing
        configuration.
    DeadLetterConfig : DeadLetterConfig, optional
        A dead-letter queue configuration for the function.
    Description : str, optional
        A description of the function.
    Environment : Environment, optional
        Environment variables that are accessible from function code during execution.
    EphemeralStorage : EphemeralStorage, optional
        The size of the function's /tmp directory in MB.
    FileSystemConfigs : List[FileSystemConfig], optional
        Connection settings for an Amazon EFS file system.
    FunctionName : str
        The name or ARN of the Lambda function.
    Handler : str, optional
        The name of the method within your code that Lambda calls to run your function.
    ImageConfig : ImageConfig, optional
        Container image configuration values that override the values in the container
        image Dockerfile.
    KMSKeyArn : str, optional
        The ARN of the AWS Key Management Service (AWS KMS) customer managed key for
        encryption.
    Layers : List[str], optional
        A list of function layers to add to the function's execution environment.
    LoggingConfig : LoggingConfig, optional
        The function's Amazon CloudWatch Logs configuration settings.
    MemorySize : int, optional
        The amount of memory available to the function at runtime.
    PackageType : str, optional
        The type of deployment package.
    Publish : bool, optional
        Set to true to publish the first version of the function during creation.
    Role : str
        The Amazon Resource Name (ARN) of the function's execution role.
    Runtime : str, optional
        The identifier of the function's runtime.
    SnapStart : SnapStart, optional
        The function's Lambda SnapStart setting.
    Tags : Dict[str, str], optional
        A list of tags to apply to the function.
    Timeout : int, optional
        The amount of time (in seconds) that Lambda allows a function to run before
        stopping it.
    TracingConfig : TracingConfig, optional
        Set Mode to Active to sample and trace a subset of incoming requests with X-Ray.
    VpcConfig : VpcConfig, optional
        For network connectivity to AWS resources in a VPC, specify a list of security
        groups and subnets.
    """

    Code: FunctionCode
    FunctionName: str
    Role: str
    Architectures: list[str] | None = None
    CodeSigningConfigArn: str | None = None
    DeadLetterConfig: DeadLetterConfigModel | None = None
    Description: str | None = None
    Environment: EnvironmentModel | None = None
    EphemeralStorage: EphemeralStorageModel | None = None
    FileSystemConfigs: list[FileSystemConfig] | None = None
    Handler: str | None = None
    ImageConfig: ImageConfigModel | None = None
    KMSKeyArn: str | None = None
    Layers: list[str] | None = None
    LoggingConfig: LoggingConfigModel | None = None
    MemorySize: int | None = None
    PackageType: str | None = None
    Publish: bool | None = None
    Runtime: str | None = None
    SnapStart: SnapStartModel | None = None
    Tags: dict[str, str] | None = None
    Timeout: int | None = None
    TracingConfig: TracingConfigModel | None = None
    VpcConfig: VpcConfigModel | None = None


class CreateFunctionResponse(BaseModel):
    """
    Response model for creating a Lambda function.

    Parameters
    ----------
    Architectures : List[str], optional
        The instruction set architecture that the function supports.
    CodeSha256 : str, optional
        The SHA256 hash of the function's deployment package.
    CodeSize : int, optional
        The size of the function's deployment package, in bytes.
    DeadLetterConfig : DeadLetterConfig, optional
        The function's dead letter queue.
    Description : str, optional
        The function's description.
    Environment : EnvironmentResponse, optional
        The function's environment variables.
    EphemeralStorage : EphemeralStorage, optional
        The size of the function's /tmp directory in MB.
    FileSystemConfigs : List[FileSystemConfig], optional
        Connection settings for an Amazon EFS file system.
    FunctionArn : str, optional
        The function's Amazon Resource Name (ARN).
    FunctionName : str, optional
        The name of the function.
    Handler : str, optional
        The function that Lambda calls to begin running your function.
    ImageConfigResponse : ImageConfigResponse, optional
        The function's image configuration values.
    KMSKeyArn : str, optional
        The ARN of the AWS Key Management Service (AWS KMS) customer managed key.
    LastModified : str, optional
        The date and time that the function was last updated.
    LastUpdateStatus : str, optional
        The status of the last update that was performed on the function.
    LastUpdateStatusReason : str, optional
        The reason for the last update that was performed on the function.
    LastUpdateStatusReasonCode : str, optional
        The reason code for the last update that was performed on the function.
    Layers : List[Layer], optional
        The function's layers.
    LoggingConfig : LoggingConfig, optional
        The function's Amazon CloudWatch Logs configuration settings.
    MasterArn : str, optional
        For Lambda@Edge functions, the ARN of the main function.
    MemorySize : int, optional
        The amount of memory available to the function at runtime.
    PackageType : str, optional
        The type of deployment package.
    RevisionId : str, optional
        The latest updated revision of the function or alias.
    Role : str, optional
        The function's execution role.
    Runtime : str, optional
        The identifier of the function's runtime.
    RuntimeVersionConfig : RuntimeVersionConfig, optional
        The ARN of the runtime and any errors that occurred.
    SigningJobArn : str, optional
        The ARN of the signing job.
    SigningProfileVersionArn : str, optional
        The ARN of the signing profile version.
    SnapStart : SnapStartResponse, optional
        The function's SnapStart setting.
    State : str, optional
        The current state of the function.
    StateReason : str, optional
        The reason for the function's current state.
    StateReasonCode : str, optional
        The reason code for the function's current state.
    Timeout : int, optional
        The amount of time in seconds that Lambda allows a function to run before
        stopping it.
    TracingConfig : TracingConfigResponse, optional
        The function's AWS X-Ray tracing configuration.
    Version : str, optional
        The version of the Lambda function.
    VpcConfig : VpcConfigResponse, optional
        The function's networking configuration.
    """

    Architectures: list[str] | None = None
    CodeSha256: str | None = None
    CodeSize: int | None = None
    DeadLetterConfig: DeadLetterConfigModel | None = None
    Description: str | None = None
    Environment: EnvironmentResponse | None = None
    EphemeralStorage: EphemeralStorageModel | None = None
    FileSystemConfigs: list[FileSystemConfig] | None = None
    FunctionArn: str | None = None
    FunctionName: str | None = None
    Handler: str | None = None
    ImageConfigResponse: ImageConfigResponseModel | None = None
    KMSKeyArn: str | None = None
    LastModified: str | None = None
    LastUpdateStatus: str | None = None
    LastUpdateStatusReason: str | None = None
    LastUpdateStatusReasonCode: str | None = None
    Layers: list[Layer] | None = None
    LoggingConfig: LoggingConfigModel | None = None
    MasterArn: str | None = None
    MemorySize: int | None = None
    PackageType: str | None = None
    RevisionId: str | None = None
    Role: str | None = None
    Runtime: str | None = None
    RuntimeVersionConfig: RuntimeVersionConfigModel | None = None
    SigningJobArn: str | None = None
    SigningProfileVersionArn: str | None = None
    SnapStart: SnapStartResponse | None = None
    State: str | None = None
    StateReason: str | None = None
    StateReasonCode: str | None = None
    Timeout: int | None = None
    TracingConfig: TracingConfigResponse | None = None
    Version: str | None = None
    VpcConfig: VpcConfigResponse | None = None
