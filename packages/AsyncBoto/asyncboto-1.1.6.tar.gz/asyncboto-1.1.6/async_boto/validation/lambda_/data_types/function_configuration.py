from typing import Annotated, Literal

from pydantic import BaseModel, Field

from .dead_letter_config import DeadLetterConfig as DeadLetterConfigModel
from .environment_response import EnvironmentResponse
from .ephemeral_storage import EphemeralStorage as EphemeralStorageModel
from .file_system_config import FileSystemConfig
from .image_config_response import ImageConfigResponse as ImageConfigResponseModel
from .layer import Layer
from .logging_config import LoggingConfig as LoggingConfigModel
from .runtime_version_config import RuntimeVersionConfig as RuntimeVersionConfigModel
from .snap_start_response import SnapStartResponse
from .tracing_config_response import TracingConfigResponse
from .vpc_config_response import VpcConfigResponse


class FunctionConfiguration(BaseModel):
    """
    Details about a Lambda function's configuration.

    Parameters
    ----------
    Architectures : Optional[List[Literal['x86_64', 'arm64']]], optional
        The instruction set architecture supported by the function.
    CodeSha256 : Optional[str], optional
        The SHA256 hash of the function's deployment package.
    CodeSize : Optional[int], optional
        The size of the function's deployment package in bytes.
    DeadLetterConfig : Optional[DeadLetterConfig], optional
        The function's dead letter queue configuration.
    Description : Optional[str], optional
        The function's description.
    Environment : Optional[EnvironmentResponse], optional
        The function's environment variables.
    EphemeralStorage : Optional[EphemeralStorage], optional
        The size of the function's /tmp directory.
    FileSystemConfigs : Optional[List[FileSystemConfig]], optional
        Connection settings for an Amazon EFS file system.
    FunctionArn : Optional[str], optional
        The function's Amazon Resource Name (ARN).
    FunctionName : Optional[str], optional
        The name of the function.
    Handler : Optional[str], optional
        The function that Lambda calls to begin running the function.
    ImageConfigResponse : Optional[ImageConfigResponse], optional
        The function's image configuration values.
    KMSKeyArn : Optional[str], optional
        The ARN of the AWS KMS key used to encrypt function resources.
    LastModified : Optional[str], optional
        The date and time the function was last updated.
    LastUpdateStatus : Optional[Literal['Successful', 'Failed', 'InProgress']], optional
        The status of the last update performed on the function.
    LastUpdateStatusReason : Optional[str], optional
        The reason for the last function update.
    LastUpdateStatusReasonCode : Optional[str], optional
        The reason code for the last function update.
    Layers : Optional[List[Layer]], optional
        The function's layers.
    LoggingConfig : Optional[LoggingConfig], optional
        The function's CloudWatch Logs configuration.
    MasterArn : Optional[str], optional
        For Lambda@Edge functions, the ARN of the main function.
    MemorySize : Optional[int], optional
        The amount of memory available to the function at runtime.
    PackageType : Optional[Literal['Zip', 'Image']], optional
        The type of deployment package.
    RevisionId : Optional[str], optional
        The latest updated revision of the function.
    Role : Optional[str], optional
        The function's execution role.
    Runtime : Optional[str], optional
        The identifier of the function's runtime.
    RuntimeVersionConfig : Optional[RuntimeVersionConfig], optional
        The ARN of the runtime and any errors.
    SigningJobArn : Optional[str], optional
        The ARN of the signing job.
    SigningProfileVersionArn : Optional[str], optional
        The ARN of the signing profile version.
    SnapStart : Optional[SnapStartResponse], optional
        The function's SnapStart setting.
    State : Optional[Literal['Pending', 'Active', 'Inactive', 'Failed']], optional
        The current state of the function.
    StateReason : Optional[str], optional
        The reason for the function's current state.
    StateReasonCode : Optional[str], optional
        The reason code for the function's current state.
    Timeout : Optional[int], optional
        The amount of time Lambda allows the function to run.
    TracingConfig : Optional[TracingConfigResponse], optional
        The function's AWS X-Ray tracing configuration.
    Version : Optional[str], optional
        The version of the Lambda function.
    VpcConfig : Optional[VpcConfigResponse], optional
        The function's networking configuration.
    """

    Architectures: list[Annotated[str, Literal["x86_64", "arm64"]]] | None = None
    CodeSha256: str | None = None
    CodeSize: int | None = None
    DeadLetterConfig: DeadLetterConfigModel | None = None
    Description: Annotated[str | None, Field(max_length=256)] = None
    Environment: EnvironmentResponse | None = None
    EphemeralStorage: EphemeralStorageModel | None = None
    FileSystemConfigs: list[FileSystemConfig] | None = None
    FunctionArn: str | None = None
    FunctionName: str | None = None
    Handler: Annotated[str | None, Field(max_length=128)] = None
    ImageConfigResponse: ImageConfigResponseModel | None = None
    KMSKeyArn: str | None = None
    LastModified: str | None = None
    LastUpdateStatus: Literal["Successful", "Failed", "InProgress"] | None = None
    LastUpdateStatusReason: str | None = None
    LastUpdateStatusReasonCode: str | None = None
    Layers: list[Layer] | None = None
    LoggingConfig: LoggingConfigModel | None = None
    MasterArn: str | None = None
    MemorySize: Annotated[int | None, Field(ge=128, le=10240)] = None
    PackageType: Literal["Zip", "Image"] | None = None
    RevisionId: str | None = None
    Role: str | None = None
    Runtime: str | None = None
    RuntimeVersionConfig: RuntimeVersionConfigModel | None = None
    SigningJobArn: str | None = None
    SigningProfileVersionArn: str | None = None
    SnapStart: SnapStartResponse | None = None
    State: Literal["Pending", "Active", "Inactive", "Failed"] | None = None
    StateReason: str | None = None
    StateReasonCode: str | None = None
    Timeout: Annotated[int | None, Field(ge=1)] = None
    TracingConfig: TracingConfigResponse | None = None
    Version: str | None = None
    VpcConfig: VpcConfigResponse | None = None
