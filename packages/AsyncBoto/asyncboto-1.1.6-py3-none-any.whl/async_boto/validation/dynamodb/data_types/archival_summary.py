from pydantic import BaseModel, Field


class ArchivalSummary(BaseModel):
    ArchivalBackupArn: str | None = Field(None, min_length=37, max_length=1024)
    ArchivalDateTime: float | None = None
    ArchivalReason: str | None = None
