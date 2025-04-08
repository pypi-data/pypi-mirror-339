from pydantic import BaseModel

from .image_config import ImageConfig as ImageConfigModel
from .image_config_error import ImageConfigError


class ImageConfigResponse(BaseModel):
    """
    Response to a GetFunctionConfiguration request containing image configuration
    details.

    Parameters
    ----------
    Error : Optional[ImageConfigError], optional
        Error response to GetFunctionConfiguration.
    ImageConfig : Optional[ImageConfig], optional
        Configuration values that override the container image Dockerfile.
    """

    Error: ImageConfigError | None = None
    ImageConfig: ImageConfigModel | None = None
