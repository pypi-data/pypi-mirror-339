from pydantic import BaseModel, constr


class GetResourcePolicyRequest(BaseModel):
    """
    Request model for the GetResourcePolicy operation.

    Attributes
    ----------
    ResourceArn : str
        The Amazon Resource Name (ARN) of the DynamoDB resource to which the policy
        is attached.
    """

    ResourceArn: constr(min_length=1, max_length=1283)


class GetResourcePolicyResponse(BaseModel):
    """
    Response model for the GetResourcePolicy operation.

    Attributes
    ----------
    Policy : str
        The resource-based policy document attached to the resource, in JSON format.
    RevisionId : str
        A unique string that represents the revision ID of the policy.
    """

    Policy: constr(min_length=1)
    RevisionId: constr(min_length=1, max_length=255)
