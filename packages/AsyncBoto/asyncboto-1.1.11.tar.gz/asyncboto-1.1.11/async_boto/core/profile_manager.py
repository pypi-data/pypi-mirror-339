import configparser
import datetime
import json
import logging
import os
import subprocess
from pathlib import Path
from typing import Any


class AWSProfileManager:
    """
    Handles AWS profiles similar to boto3 but without dependencies.
    Supports standard credential files and SSO authentication.
    """

    def __init__(self, logger=None):
        self._profiles = {}
        self._config_files = []
        self._loaded = False
        self._sso_cache = {}

        # Setup logging
        self.logger = logger or logging.getLogger("AWSProfileManager")
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

    def _get_config_file_paths(self) -> list[Path]:
        """
        Get the paths to AWS config files.
        Returns a list of paths to check for AWS profiles.
        """
        paths = []

        # Check AWS_CONFIG_FILE environment variable
        config_file = os.environ.get("AWS_CONFIG_FILE")
        if config_file:
            paths.append(Path(config_file))

        # Check AWS_SHARED_CREDENTIALS_FILE environment variable
        creds_file = os.environ.get("AWS_SHARED_CREDENTIALS_FILE")
        if creds_file:
            paths.append(Path(creds_file))

        # Default locations
        home_dir = Path.home()
        paths.append(home_dir / ".aws" / "config")
        paths.append(home_dir / ".aws" / "credentials")

        return paths

    def _load_profiles(self) -> None:
        """
        Load profiles from AWS config files.
        """
        if self._loaded:
            return

        for config_path in self._get_config_file_paths():
            if not config_path.exists():
                continue

            config = configparser.ConfigParser()
            config.read(config_path)

            self._config_files.append((config_path, config))

            for section in config.sections():
                profile_name = section

                # Handle the [profile xyz] format in config file
                if section.startswith("profile "):
                    profile_name = section[8:].strip()

                if profile_name not in self._profiles:
                    self._profiles[profile_name] = {}

                # Update with values from this section
                for key, value in config[section].items():
                    self._profiles[profile_name][key] = value

        self._loaded = True

    def get_profile(self, profile_name: str | None = None) -> dict[str, Any]:
        """
        Get a specific AWS profile.

        Args:
            profile_name: The name of the profile to get.
                          If None, will try to get the default profile
                          or use AWS environment variables.

        Returns:
            Profile data as a dictionary

        Raises:
            ValueError: If the profile doesn't exist or no default can be found
        """
        self._load_profiles()

        # If no profile specified, check environment variables
        if profile_name is None:
            profile_name = os.environ.get("AWS_PROFILE")

        # If still no profile, use default
        if profile_name is None:
            profile_name = "default"

        # Check if profile exists
        if profile_name not in self._profiles:
            raise ValueError(f"Profile '{profile_name}' not found in AWS config files")

        return self._profiles[profile_name].copy()

    def _get_sso_cache_dir(self) -> Path:
        """
        Get the directory where SSO tokens are cached

        Returns:
            Path to SSO cache directory
        """
        cache_dir = os.environ.get("AWS_SSO_CACHE_DIR")
        if cache_dir:
            return Path(cache_dir)

        return Path.home() / ".aws" / "sso" / "cache"

    def _get_sso_cached_tokens(self) -> dict[str, Any]:
        """
        Get all cached SSO tokens

        Returns:
            Dictionary of SSO tokens by start URL
        """
        cache_dir = self._get_sso_cache_dir()
        if not cache_dir.exists():
            return {}

        tokens = {}
        for file_path in cache_dir.glob("*.json"):
            try:
                with open(file_path) as f:
                    token_data = json.load(f)

                # Check for SSO token file format
                if "startUrl" in token_data:
                    tokens[token_data["startUrl"]] = token_data
            except (OSError, json.JSONDecodeError) as e:
                self.logger.warning(f"Error reading SSO token file {file_path}: {e}")

        return tokens

    def _get_sso_token(self, start_url: str, sso_region: str) -> dict[str, Any] | None:
        """
        Get a valid SSO token for the given start URL and region

        Args:
            start_url: SSO start URL
            sso_region: AWS region for SSO service

        Returns:
            Valid token data or None if not available
        """
        # Check cache first
        cache_key = f"{start_url}:{sso_region}"
        if cache_key in self._sso_cache:
            token_data = self._sso_cache[cache_key]
            expiration = datetime.datetime.fromtimestamp(token_data.get("expiresAt", 0))

            # If token is still valid, return it
            if expiration > datetime.datetime.now() + datetime.timedelta(minutes=5):
                return token_data

        # Check file cache
        tokens = self._get_sso_cached_tokens()
        token_data = tokens.get(start_url)

        if token_data:
            # Parse expiration time
            expiration_str = token_data.get("expiresAt")
            if not expiration_str:
                return None

            print(f"{expiration_str=} {token_data=}")
            try:
                if isinstance(expiration_str, int | float):
                    expiration = datetime.datetime.fromtimestamp(expiration_str)
                else:
                    # Sometimes it's stored as ISO format string
                    expiration = datetime.datetime.fromisoformat(
                        expiration_str.replace("Z", "+00:00")
                    )

                # Check if token is still valid
                if expiration > datetime.datetime.now(
                    datetime.UTC
                ) + datetime.timedelta(minutes=5):
                    self._sso_cache[cache_key] = token_data
                    return token_data
            except (ValueError, TypeError) as e:
                self.logger.warning(f"Error parsing SSO token expiration: {e}")

        # If we get here, need to refresh the token using AWS CLI
        self.logger.info(
            f"SSO token not found or expired for "
            f"{start_url}. Please run 'aws sso login'"
        )
        raise ValueError(
            f"SSO token not found or expired for "
            f"{start_url}. Please run 'aws sso login'"
        )
        # try:
        #     # Try to login using the AWS CLI
        #     subprocess.run(
        #         ["aws", "sso", "login", "--sso-session", start_url],
        #         check=True,
        #         capture_output=True,
        #     )
        #
        #     # Re-check the cache
        #     tokens = self._get_sso_cached_tokens()
        #     token_data = tokens.get(start_url)
        #
        #     if token_data:
        #         self._sso_cache[cache_key] = token_data
        #         return token_data
        #
        # except (subprocess.SubprocessError, FileNotFoundError) as e:
        #     self.logger.error(f"Failed to refresh SSO token: {e}")

        return None

    async def _get_sso_credentials_async(
        self, profile: dict[str, str], client_func
    ) -> dict[str, str]:
        """
        Get SSO credentials for a profile using the provided async client function

        Args:
            profile: Profile data
            client_func: Async function to create a client

        Returns:
            Credentials dictionary
        """
        start_url = profile.get("sso_start_url")
        sso_region = profile.get("sso_region")
        account_id = profile.get("sso_account_id")
        role_name = profile.get("sso_role_name")

        if not all([start_url, sso_region, account_id, role_name]):
            raise ValueError("Incomplete SSO configuration in profile")

        # Get SSO token
        token_data = self._get_sso_token(start_url, sso_region)
        if not token_data:
            raise ValueError("Could not get valid SSO token")

        # Make async call to SSO service to get role credentials
        try:
            # Create an SSO client
            async with await client_func("sso", sso_region) as sso_client:
                response = await sso_client.get_role_credentials(
                    accessToken=token_data["accessToken"],
                    accountId=account_id,
                    roleName=role_name,
                )

                creds = response.get("roleCredentials", {})

                return {
                    "aws_access_key_id": creds.get("accessKeyId"),
                    "aws_secret_access_key": creds.get("secretAccessKey"),
                    "aws_session_token": creds.get("sessionToken"),
                    "expiration": creds.get("expiration"),
                    "region_name": profile.get("region"),
                }
        except Exception as e:
            self.logger.error(f"Error getting SSO role credentials: {e}")
            raise ValueError(f"Failed to get SSO credentials: {e}")

    def _get_sso_credentials_sync(self, profile: dict[str, str]) -> dict[str, str]:
        """
        Get SSO credentials for a profile using subprocess to call AWS CLI

        Args:
            profile: Profile data

        Returns:
            Credentials dictionary
        """
        start_url = profile.get("sso_start_url")
        sso_region = profile.get("sso_region")
        account_id = profile.get("sso_account_id")
        role_name = profile.get("sso_role_name")

        if not all([start_url, sso_region, account_id, role_name]):
            raise ValueError("Incomplete SSO configuration in profile")

        # Get SSO token
        token_data = self._get_sso_token(start_url, sso_region)
        if not token_data:
            raise ValueError("Could not get valid SSO token")

        # Use AWS CLI to get credentials
        try:
            result = subprocess.run(
                [
                    "aws",
                    "sso",
                    "get-role-credentials",
                    "--profile",
                    profile.get("__name__", "default"),
                    "--region",
                    sso_region,
                    "--account-id",
                    account_id,
                    "--role-name",
                    role_name,
                    "--access-token",
                    token_data["accessToken"],
                    "--output",
                    "json",
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            response = json.loads(result.stdout)
            creds = response.get("roleCredentials", {})

            return {
                "aws_access_key_id": creds.get("accessKeyId"),
                "aws_secret_access_key": creds.get("secretAccessKey"),
                "aws_session_token": creds.get("sessionToken"),
                "expiration": creds.get("expiration"),
                "region_name": profile.get("region"),
            }
        except (
            subprocess.SubprocessError,
            json.JSONDecodeError,
            FileNotFoundError,
        ) as e:
            self.logger.error(f"Error getting SSO role credentials: {e}")
            raise ValueError(f"Failed to get SSO credentials: {e}")

    def get_credentials(self, profile_name: str | None = None) -> dict[str, str]:
        """
        Get AWS credentials from profile or environment variables

        Args:
            profile_name: The name of the profile to get credentials from.
                          If None, will try to get the default profile
                          or use AWS environment variables.

        Returns:
            Dictionary with aws_access_key_id, aws_secret_access_key,
            aws_session_token (if available), and region_name (if available)
        """
        # Check environment variables first (they take precedence)
        credentials = {}

        # Check for access key in environment
        access_key = os.environ.get("AWS_ACCESS_KEY_ID")
        if access_key:
            credentials["aws_access_key_id"] = access_key

            # If access key is in environment, also check for secret key
            secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
            if secret_key:
                credentials["aws_secret_access_key"] = secret_key

                # If both keys found, also check for session token
                session_token = os.environ.get("AWS_SESSION_TOKEN")
                if session_token:
                    credentials["aws_session_token"] = session_token

        # Check for region in environment
        region = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
        if region:
            credentials["region_name"] = region

        # If we have all required credentials from environment, return them
        if (
            "aws_access_key_id" in credentials
            and "aws_secret_access_key" in credentials
        ):
            return credentials

        # Otherwise, try to get from profile
        try:
            profile = self.get_profile(profile_name)

            # Store profile name for reference
            profile["__name__"] = profile_name or "default"

            # Check if this is an SSO profile
            if "sso_start_url" in profile:
                self.logger.info(
                    f"Using SSO authentication for profile {profile['__name__']}"
                )
                # For synchronous credential retrieval, use subprocess with AWS CLI
                return self._get_sso_credentials_sync(profile)

            # Map profile keys to credential keys
            key_mapping = {
                "aws_access_key_id": ["aws_access_key_id", "access_key_id"],
                "aws_secret_access_key": ["aws_secret_access_key", "secret_access_key"],
                "aws_session_token": ["aws_session_token", "session_token"],
                "region_name": ["region"],
            }

            # Some profiles may use different key names
            for cred_key, profile_keys in key_mapping.items():
                for profile_key in profile_keys:
                    if profile_key in profile and cred_key not in credentials:
                        credentials[cred_key] = profile[profile_key]

            # Handle assume role if specified in profile
            if "role_arn" in profile:
                # This would involve making an STS call to assume the role
                # For now, we'll raise an error as this requires additional
                # implementation
                raise NotImplementedError(
                    "Assuming roles from profiles requires STS implementation"
                )

        except ValueError:
            # If no profile found and no environment credentials, just return empty dict
            pass

        # Validate we have the minimum required credentials
        if not (
            "aws_access_key_id" in credentials
            and "aws_secret_access_key" in credentials
        ):
            raise ValueError(
                "No valid AWS credentials found in environment or profiles"
            )

        return credentials

    async def get_credentials_async(
        self, profile_name: str | None = None, client_func=None
    ) -> dict[str, str]:
        """
        Get AWS credentials asynchronously

        Args:
            profile_name: The name of the profile to get credentials from
            client_func: Function to create an async client

        Returns:
            Credentials dictionary
        """
        # Check environment variables first
        credentials = {}

        # Check for access key in environment
        access_key = os.environ.get("AWS_ACCESS_KEY_ID")
        if access_key:
            credentials["aws_access_key_id"] = access_key

            # If access key is in environment, also check for secret key
            secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
            if secret_key:
                credentials["aws_secret_access_key"] = secret_key

                # If both keys found, also check for session token
                session_token = os.environ.get("AWS_SESSION_TOKEN")
                if session_token:
                    credentials["aws_session_token"] = session_token

        # Check for region in environment
        region = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
        if region:
            credentials["region_name"] = region

        # If we have all required credentials from environment, return them
        if (
            "aws_access_key_id" in credentials
            and "aws_secret_access_key" in credentials
        ):
            return credentials

        # Otherwise, try to get from profile
        try:
            profile = self.get_profile(profile_name)

            # Store profile name for reference
            profile["__name__"] = profile_name or "default"

            # Check if this is an SSO profile
            if "sso_start_url" in profile and client_func:
                self.logger.info(
                    f"Using SSO authentication for profile {profile['__name__']}"
                )
                return await self._get_sso_credentials_async(profile, client_func)
            elif "sso_start_url" in profile:
                self.logger.info(
                    f"Using SSO authentication for profile {profile['__name__']}"
                )
                # Fall back to sync method if client_func not provided
                return self._get_sso_credentials_sync(profile)

            # Map profile keys to credential keys
            key_mapping = {
                "aws_access_key_id": ["aws_access_key_id", "access_key_id"],
                "aws_secret_access_key": ["aws_secret_access_key", "secret_access_key"],
                "aws_session_token": ["aws_session_token", "session_token"],
                "region_name": ["region"],
            }

            # Some profiles may use different key names
            for cred_key, profile_keys in key_mapping.items():
                for profile_key in profile_keys:
                    if profile_key in profile and cred_key not in credentials:
                        credentials[cred_key] = profile[profile_key]

            # Handle assume role if specified in profile
            if "role_arn" in profile:
                raise NotImplementedError(
                    "Assuming roles from profiles requires STS implementation"
                )

        except ValueError:
            # If no profile found and no environment credentials, just return empty dict
            pass

        # Validate we have the minimum required credentials
        if not (
            "aws_access_key_id" in credentials
            and "aws_secret_access_key" in credentials
        ):
            raise ValueError(
                "No valid AWS credentials found in environment or profiles"
            )

        return credentials

    def list_profiles(self) -> list[str]:
        """
        List all available AWS profiles

        Returns:
            List of profile names
        """
        self._load_profiles()
        return list(self._profiles.keys())

    def get_available_regions(self, service_name: str = "s3") -> list[str]:
        """
        Get available regions for a service.
        This is a simplified implementation that returns common regions.

        Args:
            service_name: AWS service name (ignored in this implementation)

        Returns:
            List of region names
        """
        # This is a simplified list of common regions
        # A full implementation would need to check AWS's region data
        return [
            "us-east-1",
            "us-east-2",
            "us-west-1",
            "us-west-2",
            "ca-central-1",
            "eu-west-1",
            "eu-west-2",
            "eu-west-3",
            "eu-central-1",
            "eu-north-1",
            "ap-northeast-1",
            "ap-northeast-2",
            "ap-northeast-3",
            "ap-southeast-1",
            "ap-southeast-2",
            "ap-south-1",
            "sa-east-1",
        ]
