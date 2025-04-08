from pydantic import BaseModel, constr

from .data_types.code_signing_config import CodeSigningConfig as CodeSigningConfigModel


class GetCodeSigningConfigRequest(BaseModel):
    """
    Request model for retrieving information about a code signing configuration.

    Attributes
    ----------
    CodeSigningConfigArn : str
        The ARN of the code signing configuration.
    """

    CodeSigningConfigArn: constr(
        max_length=200,
        pattern=r"arn:(aws[a-zA-Z-]*)?:lambda:[a-z]{2}((-gov)|(-iso(b?)))?-[a-z]+-\d{1}:\d{12}:code-signing-config:csc-[a-z0-9]{17}",
    )


class GetCodeSigningConfigResponse(BaseModel):
    """
    Response model for retrieving information about a code signing configuration.

    Attributes
    ----------
    CodeSigningConfig : CodeSigningConfig
        The code signing configuration.
    """

    CodeSigningConfig: CodeSigningConfigModel
