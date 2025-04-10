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


def get_valid_until():
    valid_until = date.today() + timedelta(days=30)
    return valid_until


class SubmissionTbl(SQLModel, table=True):
    __tablename__ = "submission"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        sa_column_kwargs={"server_default": text("gen_random_uuid()")},
        nullable=False,
        index=True,
    )
    user_account_id: UUID = Field(foreign_key="user.id", ondelete="CASCADE")
    project_id: UUID = Field(foreign_key="project.id", ondelete="CASCADE")
    validated: bool = Field(
        default=False,
        sa_column_kwargs={
            "server_default": "false",
        },
        nullable=False,
    )
    created_at: datetime = Field(sa_column_kwargs={"server_default": func.now()})
    expires_at: datetime = Field(default_factory=get_valid_until)
    updated_at: datetime = Field(
        sa_column_kwargs={"server_default": func.now(), "onupdate": func.now()}
    )
    # project: "ProjectTbl" = Relationship()
