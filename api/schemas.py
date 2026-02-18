from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class UploadResponse(BaseModel):
    dataset_id: int
    job_id: int = Field(validation_alias="id")
    status: str

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class JobResponse(BaseModel):
    status: str
    created_at: datetime


class SingleJobResponse(JobResponse):
    id: int
    dataset_id: int
    error_message: str | None
    started_at: datetime | None
    finished_at: datetime | None
