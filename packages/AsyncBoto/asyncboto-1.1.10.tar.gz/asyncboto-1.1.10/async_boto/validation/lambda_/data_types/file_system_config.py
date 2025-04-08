# ruff: noqa: E501
from typing import Annotated

from pydantic import BaseModel, Field


class FileSystemConfig(BaseModel):
    """
    Details about the connection between a Lambda function and an Amazon EFS file system.

    Parameters
    ----------
    Arn : str
        The Amazon Resource Name (ARN) of the Amazon EFS access point that provides access to the file system.
    LocalMountPath : str
        The path where the function can access the file system, starting with /mnt/.
    """

    Arn: Annotated[
        str,
        Field(
            max_length=200,
            pattern=r"arn:aws[a-zA-Z-]*:elasticfilesystem:[a-z]{2}((-gov)|(-iso(b?)))?-[a-z]+-\d{1}:\d{12}:access-point/fsap-[a-f0-9]{17}",
        ),
    ]
    LocalMountPath: Annotated[
        str, Field(max_length=160, pattern=r"^/mnt/[a-zA-Z0-9-_.]+$")
    ]
