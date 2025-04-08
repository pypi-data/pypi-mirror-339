from pydantic import BaseModel


class Environment(BaseModel):
    """
    A function's environment variable settings.

    Environment variables allow you to adjust your Lambda function's behavior without
    updating code. Variables are stored as key-value pairs that are available to your
    code during function execution.

    Parameters
    ----------
    Variables : Optional[Dict[str, str]]
        Environment variable key-value pairs for the Lambda function.

        These are accessible from function code during execution. For example,
        in Node.js you can access environment variables using `process.env.KEY_NAME`,
        and in Python using `os.environ['KEY_NAME']`.

        Common uses include:
        - Configuration parameters that vary between environments
        - Secrets and API keys (though AWS Secrets Manager is preferred for sensitive
        values)
        - Feature flags
        - Connection strings

        Constraints:
        - Keys must start with a letter and contain only letters, numbers,
        and underscore
        - Keys are case-sensitive
        - The size of the environment variables (including keys and values) must not
          exceed the overall limit (typically 4 KB)
        - Cannot include AWS reserved environment variables (e.g., AWS_REGION, etc.)
    """

    Variables: dict[str, str] | None = None
