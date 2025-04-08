from pydantic import BaseModel, conlist


class VpcConfig(BaseModel):
    """
    The VPC security groups and subnets that are attached to a Lambda function.
    For more information, see Configuring a Lambda function to access resources in a
    VPC.

    Attributes
    ----------
    Ipv6AllowedForDualStack : Optional[bool]
        Allows outbound IPv6 traffic on VPC functions that are connected to
        dual-stack subnets.
    SecurityGroupIds : Optional[conlist(str, max_items=5)]
        A list of VPC security group IDs.
    SubnetIds : Optional[conlist(str, max_items=16)]
        A list of VPC subnet IDs.
    """

    Ipv6AllowedForDualStack: bool | None = None
    SecurityGroupIds: conlist(str, max_length=5) | None = None
    SubnetIds: conlist(str, max_length=16) | None = None
