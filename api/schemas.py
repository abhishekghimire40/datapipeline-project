from pydantic import BaseModel, ConfigDict, Field


class UploadResponse(BaseModel):
    dataset_id: int
    job_id: int = Field(validation_alias="id")
    status: str

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
