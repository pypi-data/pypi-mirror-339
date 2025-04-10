from uuid import uuid4, UUID
from datetime import datetime

from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy.dialects.postgresql import JSONB

from sqlalchemy import (
    func,
    text,
)


class ProjectTbl(SQLModel, table=True):
    __tablename__ = "project"

    id: UUID = Field(
        primary_key=True,
        default_factory=uuid4,
        sa_column_kwargs={
            "server_default": text("gen_random_uuid()"),
        },
    )
    owner_id: UUID = Field(foreign_key="user.id", nullable=False)
    title: str = Field(max_length=50)
    description: str
    proj_inputs: dict = Field(sa_type=JSONB, nullable=False)
    created_at: datetime = Field(
        sa_column_kwargs={"server_default": func.now(), "onupdate": func.now()}
    )
    updated_at: datetime = Field(
        sa_column_kwargs={"server_default": func.now(), "onupdate": func.now()}
    )

    owner: "UserTbl" = Relationship(back_populates="user_projects")
