from uuid import UUID, uuid4
from datetime import datetime

from sqlmodel import SQLModel, Field, Relationship

from sqlalchemy import (
    func,
    text,
)

from . import access_control


class UserTbl(SQLModel, table=True):
    __tablename__ = "user"

    id: UUID = Field(
        primary_key=True,
        default_factory=uuid4,
    )
    username: str | None
    email: str = Field(max_length=255, index=True)
    image: str | None
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"onupdate": func.now(), "server_default": func.now()},
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"onupdate": func.now(), "server_default": func.now()},
    )

    # Relationships
    user_projects: list["ProjectTbl"] = Relationship(back_populates="owner")
    user_roles: list["RoleTbl"] = Relationship(  # type: ignore
        link_model=access_control.UserRoleLinkTbl
    )
    accounts: list["UserAccountTbl"] = Relationship(back_populates="user")
    reusable_preview_credits: list["ReusablePreviewTokenTbl"] = Relationship(
        back_populates="user"
    )

    def __repr__(self):
        return f"User(id={self.id!r}, email={self.email!r})"


# ------------------
# -- Child tables --
# ------------------


# One user may have multiple 'accounts' (login methods e.g. Google, Github, Email)
class UserAccountTbl(SQLModel, table=True):
    __tablename__ = "oauth_account"

    # id: Mapped[int] = mapped_column(primary_key=True)
    id: UUID = Field(
        primary_key=True,
        index=True,
        default_factory=uuid4,
        sa_column_kwargs={
            "server_default": text("gen_random_uuid()"),
        },
    )
    user_id: UUID = Field(
        foreign_key="user.id",
        ondelete="CASCADE",
    )
    provider_id: str = Field(max_length=255)
    provider_user_id: str = Field(max_length=255)

    user: "UserTbl" = Relationship(back_populates="accounts")
