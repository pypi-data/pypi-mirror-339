from pydantic import BaseModel, constr


class PutResourcePolicyRequest(BaseModel):
    """
    Request model for the PutResourcePolicy operation.

    Attributes
    ----------
    Policy : str
        An AWS resource-based policy document in JSON format.
    ResourceArn : str
        The Amazon Resource Name (ARN) of the DynamoDB resource to which the
        policy will be attached.
    ConfirmRemoveSelfResourceAccess : Optional[bool]
        Set this parameter to true to confirm that you want to remove your permissions
        to change the policy of this resource in the future.
    ExpectedRevisionId : Optional[str]
        A string value that you can use to conditionally update your policy.
    """

    Policy: constr(min_length=1, max_length=20480)
    ResourceArn: constr(min_length=1, max_length=1283)
    ConfirmRemoveSelfResourceAccess: bool | None = None
    ExpectedRevisionId: constr(min_length=1, max_length=255) | None = None


class PutResourcePolicyResponse(BaseModel):
    """
    Response model for the PutResourcePolicy operation.

    Attributes
    ----------
    RevisionId : str
        A unique string that represents the revision ID of the policy.
    """

    RevisionId: constr(min_length=1, max_length=255)
