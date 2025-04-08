from pydantic import BaseModel, constr

from .data_types.dead_letter_config import DeadLetterConfig
from .data_types.environment_response import EnvironmentResponse
from .data_types.ephemeral_storage import EphemeralStorage
from .data_types.file_system_config import FileSystemConfig
from .data_types.image_config_response import ImageConfigResponse
from .data_types.layer import Layer
from .data_types.logging_config import LoggingConfig
from .data_types.runtime_version_config import RuntimeVersionConfig
from .data_types.snap_start_response import SnapStartResponse
from .data_types.tracing_config_response import TracingConfigResponse
from .data_types.vpc_config_response import VpcConfigResponse


class UpdateFunctionCodeRequest(BaseModel):
    FunctionName: constr(
        min_length=1,
        max_length=140,
        pattern=r"(arn:(aws[a-zA-Z-]*)?:lambda:)?([a-z]{2}(-gov)?-[a-z]+-\d{1}:)?(\d{12}:)?(function:)?([a-zA-Z0-9-_]+)(:(\$LATEST|[a-zA-Z0-9-_]+))?",  # noqa: E501
    )
    Architectures: list[constr(pattern=r"x86_64|arm64")] | None
    DryRun: bool | None
    ImageUri: str | None
    Publish: bool | None
    RevisionId: str | None
    S3Bucket: constr(min_length=3, max_length=63) | None  # noqa: E501
    S3Key: constr(min_length=1, max_length=1024) | None
    S3ObjectVersion: constr(min_length=1, max_length=1024) | None
    SourceKMSKeyArn: str | None
    ZipFile: bytes | None


class UpdateFunctionCodeResponse(BaseModel):
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
