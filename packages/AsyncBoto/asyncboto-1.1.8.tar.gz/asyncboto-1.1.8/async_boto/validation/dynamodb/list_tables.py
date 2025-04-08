from pydantic import BaseModel, Field


class ListTablesRequest(BaseModel):
    ExclusiveStartTableName: str | None = Field(
        None, min_length=3, max_length=255, pattern=r"[a-zA-Z0-9_.-]+"
    )
    Limit: int | None = Field(None, ge=1, le=100)


class ListTablesResponse(BaseModel):
    LastEvaluatedTableName: str | None = Field(
        None, min_length=3, max_length=255, pattern=r"[a-zA-Z0-9_.-]+"
    )
    TableNames: list[str] = Field(..., min_length=1, max_length=100)
