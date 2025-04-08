from pydantic import BaseModel


class EphemeralStorage(BaseModel):
    """
    The size of the function's /tmp directory in MB.

    Parameters
    ----------
    Size : int
        The size of the function's /tmp directory.
        Valid range from 512 to 10240 MB.
    """

    Size: int
