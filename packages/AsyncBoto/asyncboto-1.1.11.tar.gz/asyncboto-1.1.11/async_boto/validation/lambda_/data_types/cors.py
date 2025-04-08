from pydantic import BaseModel, Field


class Cors(BaseModel):
    """
    The cross-origin resource sharing (CORS) settings for a Lambda function URL.

    CORS defines how a function URL responds to cross-origin requests, controlling
    access from different domains, protocols, or ports. These settings help implement
    security while still allowing legitimate cross-origin requests.

    Parameters
    ----------
    AllowCredentials : Optional[bool]
        Whether to allow cookies or other credentials in requests to your function URL.
        When true, cookies and authentication headers are permitted in requests.
        When false (default), credentials are rejected.

        Warning: Setting this to true while also setting AllowOrigins to "*"
        (all origins)
        is a security risk, as it allows any website to send authenticated requests to
        your function URL.

    AllowHeaders : Optional[List[str]]
        The HTTP headers that origins can include in requests to your function URL.
        Browsers typically require these headers to be included in the
        Access-Control-Allow-Headers response header for cross-origin requests.

        Examples: "Date", "Keep-Alive", "X-Custom-Header"
        Maximum items: 100

    AllowMethods : Optional[List[str]]
        The HTTP methods that are allowed when calling your function URL.
        Specifies which HTTP methods (e.g., GET, POST, PUT, DELETE) can be used
        in cross-origin requests.

        Examples: "GET", "POST", "DELETE", or "*" (for all methods)
        Maximum items: 6

    AllowOrigins : Optional[List[str]]
        The origins that can access your function URL.
        Specifies which domains can access your Lambda function URL.

        Examples:
        - Specific origins: ["https://www.example.com", "http://localhost:60905"]
        - All origins: ["*"]

        Minimum length: 1
        Maximum length: 253
        Maximum items: 100

    ExposeHeaders : Optional[List[str]]
        The HTTP headers in your function response that you want to expose to origins
        that call your function URL.

        These headers will be included in the Access-Control-Expose-Headers response
        header, making them accessible to client-side JavaScript.

        Examples: "Date", "Keep-Alive", "X-Custom-Header"
        Maximum items: 100

    MaxAge : Optional[int]
        The maximum amount of time, in seconds, that web browsers can cache results
        of a preflight request (OPTIONS request).

        By default, this is set to 0, which means the browser doesn't cache results.
        Setting a longer time reduces the number of preflight requests but may delay
        the propagation of CORS configuration changes.

        Minimum value: 0
        Maximum value: 86400 (24 hours)
    """

    AllowCredentials: bool | None = None
    AllowHeaders: list[str] | None = Field(None, max_length=100)
    AllowMethods: list[str] | None = Field(None, max_length=6)
    AllowOrigins: list[str] | None = Field(None, max_length=100)
    ExposeHeaders: list[str] | None = Field(None, max_length=100)
    MaxAge: int | None = Field(None, ge=0, le=86400)
