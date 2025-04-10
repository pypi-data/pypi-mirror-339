from uuid import uuid4, UUID
from datetime import datetime

from sqlmodel import SQLModel, Field, Relationship

from sqlalchemy import (
    func,
    text,
)

# from ceonstock_db.models.base import Base
# from ceonstock_db.models.user import UserAccountTbl


# Token to allow users to get free preview renders.
# They automatically refresh after a fixed time.
# Spent tokens are automatically refreshed if the user purchases the project.
class ReusablePreviewTokenTbl(SQLModel, table=True):
    __tablename__ = "reusable_preview_token"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        sa_column_kwargs={
            "server_default": text("gen_random_uuid()"),
        },
    )
    # Changed to regular id for compatability with oauth workflow, but left uuid naming convention to prevent
    # breakage
    user_account_id: UUID = Field(
        foreign_key="user.id",
        ondelete="CASCADE",
        nullable=False,
    )
    # Remember the project which this token was last spent on.
    project_id: UUID | None = Field(
        foreign_key="project.id",
        ondelete="SET NULL",
    )
    created_at: datetime = Field(sa_column_kwargs={"server_default": func.now()})
    available_at: datetime = Field(sa_column_kwargs={"server_default": func.now()})
    user: "UserTbl" = Relationship(back_populates="reusable_preview_credits")
