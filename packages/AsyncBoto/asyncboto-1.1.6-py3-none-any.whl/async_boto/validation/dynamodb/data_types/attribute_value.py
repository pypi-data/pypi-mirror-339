from pydantic import BaseModel, RootModel

from async_boto.utils.dynamo_conversion import from_dynamodb_json, to_dynamodb_json


class AttributeValue(BaseModel):
    S: str | None = None
    N: str | None = None
    B: bytes | None = None
    SS: list[str] | None = None
    NS: list[str] | None = None
    BS: list[bytes] | None = None
    M: dict[str, "AttributeValue"] | None = None
    L: list["AttributeValue"] | None = None
    NULL: bool | None = None
    BOOL: bool | None = None


AttributeValue.model_rebuild()


class AttributeValueDict(RootModel[dict[str, AttributeValue]]):
    @classmethod
    def from_python_dict(cls, data: dict):
        return cls(**to_dynamodb_json(data))

    def to_python_dict(self):
        return from_dynamodb_json(
            self.model_dump(exclude_none=True, exclude_defaults=True)
        )
