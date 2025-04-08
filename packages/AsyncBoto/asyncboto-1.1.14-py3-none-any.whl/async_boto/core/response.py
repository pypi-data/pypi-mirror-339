from typing import Any

from .errors import ErrorFactory


class AsyncRequestResponse:
    """
    Class to create a response object, which allows
    to retrieve async response outside the asyncio loop.

    Parameters
    ----------
    status_code : int
        status code from request.
    url : str
        the url that was requested.
    json : dict, optional
        the request json object, by default None
    text : bytes, optional
        the response as text, by default None
    """

    def __init__(
        self,
        status_code: int,
        url: str,
        headers: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        text: str | None = None,
    ):
        self.url = url
        self._status_code = status_code
        self._text = text
        self._json = json
        self._headers = headers

    @property
    def json(self):
        return self._json

    @property
    def content(self):
        return self._text

    @property
    def status_code(self):
        return self._status_code

    @property
    def headers(self):
        return self._headers

    def raise_for_status(self):
        """
        Method to raise a APIResponseError, if the status code of a request is
        higher 400.

        Raises
        ------
        APIResponseError
            if status code is >= 400
        """
        if self.status_code >= 300:
            ErrorFactory.raise_error_from_json(self.json)
