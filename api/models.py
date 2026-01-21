from __future__ import (
    annotations,
)  # helps for forward referencing for older python versions

from datetime import UTC, datetime
import enum

from database import Base
from sqlalchemy import JSON, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Dataset(Base):
    __tablename__ = "datasets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    original_file_name: Mapped[str] = mapped_column(String(100), nullable=False)
    stored_path: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )

    # forward referencing ETLJob table even before is created
    # creating one to many relationship with etl_jobs table
    jobs: Mapped[list[ETLJob]] = relationship(back_populates="dataset")


# enums for job status in ETLJob table
class Status(enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


class ETLJob(Base):
    __tablename__ = "etl_jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    dataset_id: Mapped[int] = mapped_column(
        ForeignKey("datasets.id"), index=True, nullable=False
    )

    status: Mapped[Status] = mapped_column(Enum(Status), nullable=False, index=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    finished_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    stats_json: Mapped[dict] = mapped_column(JSON, default=dict)

    # creating many to one relationship with datasets table
    dataset: Mapped[Dataset] = relationship(back_populates="jobs")
