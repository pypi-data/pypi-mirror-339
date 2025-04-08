from typing import Annotated

from pydantic import BaseModel, Field


class ImageConfig(BaseModel):
    """
    Configuration values that override the container image Dockerfile settings.

    Parameters
    ----------
    Command : Optional[List[str]], optional
        Parameters to pass in with ENTRYPOINT.
    EntryPoint : Optional[List[str]], optional
        The entry point to the application,
        typically the location of the runtime executable.
    WorkingDirectory : Optional[str], optional
        The working directory for the container.
    """

    Command: Annotated[list[str] | None, Field(max_length=1500)] = None
    EntryPoint: Annotated[list[str] | None, Field(max_length=1500)] = None
    WorkingDirectory: Annotated[str | None, Field(max_length=1000)] = None
