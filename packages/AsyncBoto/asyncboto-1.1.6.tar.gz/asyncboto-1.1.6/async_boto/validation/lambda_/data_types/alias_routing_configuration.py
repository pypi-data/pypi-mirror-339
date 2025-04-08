from pydantic import BaseModel


class AliasRoutingConfiguration(BaseModel):
    """
    The traffic-shifting configuration of a Lambda function alias.

    Allows for weighted distribution of traffic between two Lambda function versions.
    This enables implementation of canary deployments and blue/green deployment
    patterns.

    Parameters
    ----------
    AdditionalVersionWeights : Optional[Dict[str, float]]
        Mapping of version numbers to weights for traffic distribution.
        The keys are version numbers (as strings) identifying function versions.
        The values are weights (as floats between 0.0 and 1.0) representing the
        percentage of traffic to route to each specified version.

        For example, {"2": 0.1} routes 10% of traffic to version 2, while the
        remaining 90% goes to the primary version specified in the alias's
        FunctionVersion property.

        When not specified, 100% of traffic is routed to the primary version.
    """

    AdditionalVersionWeights: dict[str, float] | None = None
