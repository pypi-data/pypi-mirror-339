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


class GetFunctionConfigurationRequest(BaseModel):
    """
    Request model for retrieving the version-specific settings of a Lambda function or
    version.

    Attributes
    ----------
    FunctionName : str
        The name or ARN of the Lambda function, version, or alias.
    Qualifier : str
        Specify a version or alias to get details about a published version of the
        function.
    """

    FunctionName: constr(
        min_length=1,
        max_length=170,
        pattern=r"(arn:(aws[a-zA-Z-]*)?:lambda:)?([a-z]{2}(-gov)?-[a-z]+-\d{1}:)?(\d{12}:)?(function:)?([a-zA-Z0-9-_\.]+)(:(\$LATEST|[a-zA-Z0-9-_]+))?",  # noqa: E501
    )
    Qualifier: constr(min_length=1, max_length=128, pattern=r"(|[a-zA-Z0-9$_-]+)")


class GetFunctionConfigurationResponse(BaseModel):
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
