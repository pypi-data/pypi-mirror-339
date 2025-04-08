from pydantic import BaseModel


class DeleteCodeSigningConfigRequest(BaseModel):
    """
    Request model for deleting a Lambda code signing configuration.

    Parameters
    ----------
    CodeSigningConfigArn : str
        The Amazon Resource Name (ARN) of the code signing configuration to delete.
    """

    # URI Request Parameters
    CodeSigningConfigArn: str


class DeleteCodeSigningConfigResponse(BaseModel):
    """
    Response model for deleting a Lambda code signing configuration.

    The DeleteCodeSigningConfig operation doesn't return any data. A successful response
    returns an HTTP 204 status code with an empty HTTP body.
    """

    pass
