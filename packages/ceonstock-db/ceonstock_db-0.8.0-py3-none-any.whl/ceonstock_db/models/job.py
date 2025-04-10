from uuid import uuid4, UUID
from datetime import date, timedelta, datetime

from sqlmodel import SQLModel, Field

from sqlalchemy import (
    # Integer,
    # String,
    # JSON,
    # Boolean,
    # DateTime,
    # ForeignKey,
    func,
    text,
)
# from sqlalchemy.orm import Mapped
# from sqlalchemy.orm import mapped_column
# from sqlalchemy.orm import relationship

# from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID

# from .base import Base


def get_valid_until():
    valid_until = date.today() + timedelta(days=30)
    return valid_until


class JobTbl(SQLModel, table=True):
    __tablename__ = "job"

    id: UUID = Field(
        primary_key=True,
        default_factory=uuid4,
        index=True,
        sa_column_kwargs={
            "server_default": text("gen_random_uuid()"),
        },
    )
    user_account_id: UUID = Field(foreign_key="user.id", ondelete="CASCADE")
    project_id: UUID = Field(foreign_key="project.id", ondelete="CASCADE")
    submission_id: UUID = Field(
        # UUID(as_uuid=True),
        foreign_key="submission.id",
        ondelete="SET NULL",
        nullable=True,
    )
    # TODO allow type checking to enforce enum?
    job_type: str = Field(max_length=30, nullable=False)
    # job_type: Mapped[CstockJob.job_types] = mapped_column(max_length=30, nullable=False)
    # foreign_key="submission.id", ondelete="SET NULL"),
    created_at: datetime = Field(sa_column_kwargs={"server_default": func.now()})
    updated_at: datetime = Field(
        sa_column_kwargs={
            "onupdate": func.now(),
            "server_default": func.now(),
        },
    )
    ended_at: datetime = Field(nullable=True)
    success: bool = Field(nullable=True)

    # project: "ProjectTbl" = Relationship()
    # user_account: "UserTbl" = Relationship()


class JobProgressTbl(SQLModel, table=True):
    __tablename__ = "job_progress"

    job_id: UUID = Field(
        foreign_key="job.id",
        ondelete="CASCADE",
        primary_key=True,
    )
    assigned_to_node: str = Field(nullable=True)
    assigned_at: datetime = Field(nullable=True)
    started_at: datetime = Field(nullable=True)
    create_job_inputs_start: datetime = Field(nullable=True)
    create_job_inputs_end: datetime = Field(nullable=True)
    prepare_files_start: datetime = Field(nullable=True)
    prepare_files_end: datetime = Field(nullable=True)
    render_submit_start: datetime = Field(nullable=True)
    render_submit_end: datetime = Field(nullable=True)
    wait_for_render_start: datetime = Field(nullable=True)
    wait_for_render_end: datetime = Field(nullable=True)
    upload_outputs_start: datetime = Field(nullable=True)
    upload_outputs_end: datetime = Field(nullable=True)
    updated_at: datetime = Field(
        sa_column_kwargs={
            "onupdate": func.now(),
            "server_default": func.now(),
        },
    )


# TODO setup this by converting TIMESTAMP objects to strings then to datetime objects?
"""
job_progress_tbl.d.latest_timestamp = (
    func.max(
        [
            job_progress_tbl.c.started_at,
            job_progress_tbl.c.render_submit_start,
            job_progress_tbl.c.render_complete_confirmed,
            job_progress_tbl.c.upload_outputs_start,
            job_progress_tbl.c.ended_at,
        ]
    )
).label("latest_timestamp")
"""
# Can be late accessed as job_progress_tbl.d.latest_timestamp as though it were a real column
