from .profile_manager import AWSProfileManager


class Credentials:
    def __init__(
        self,
        aws_access_key_id: str,
        aws_secret_access_key: str,
        aws_session_token: str | None = None,
        **kwargs,
    ):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.aws_session_token = aws_session_token

    @property
    def secret_key(self) -> str:
        return self.aws_secret_access_key

    @property
    def access_key(self) -> str:
        return self.aws_access_key_id

    @property
    def token(self) -> str | None:
        return self.aws_session_token


class AsyncAWSSession:
    """
    An asynchronous AWS Session that uses aiohttp instead of boto3.
    """

    def __init__(
        self,
        aws_access_key_id: str | None = None,
        aws_secret_access_key: str | None = None,
        aws_session_token: str | None = None,
        region_name: str | None = None,
        profile_name: str | None = None,
    ):
        """
        Initialize an AsyncAWSSession with credentials

        Args:
            aws_access_key_id: AWS access key ID
            aws_secret_access_key: AWS secret access key
            aws_session_token: AWS temporary session token
            region_name: Default region when creating new connections
            profile_name: The name of a profile to use
        """
        self._profile_manager = AWSProfileManager()

        # If specific credentials are provided, use them
        if aws_access_key_id and aws_secret_access_key:
            self._credentials = {
                "aws_access_key_id": aws_access_key_id,
                "aws_secret_access_key": aws_secret_access_key,
            }
            if aws_session_token:
                self._credentials["aws_session_token"] = aws_session_token
            if region_name:
                self._credentials["region_name"] = region_name
        else:
            # Otherwise, try to get credentials from profile or environment
            self._credentials = self._profile_manager.get_credentials(profile_name)

        # If region not in credentials, use default
        if "region_name" not in self._credentials and region_name:
            self._credentials["region_name"] = region_name

        # Default to us-east-1 if no region specified
        if "region_name" not in self._credentials:
            self._credentials["region_name"] = "us-east-1"

        # Store profile name
        self._profile_name = profile_name

    @property
    def profile_name(self) -> str | None:
        """
        Get the name of the profile used for this session
        """
        return self._profile_name

    @property
    def region_name(self) -> str | None:
        """
        Get the region name for this session
        """
        return self._credentials.get("region_name")

    @property
    def available_regions(self) -> list[str] | None:
        """
        Get the available regions for this session
        """
        return self._profile_manager.get_available_regions()

    def get_credentials(self) -> Credentials:
        return Credentials(**self._credentials)
