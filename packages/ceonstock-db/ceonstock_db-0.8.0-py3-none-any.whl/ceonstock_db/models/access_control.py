from uuid import uuid4, UUID

from sqlmodel import SQLModel, Field, Relationship

# import sqlalchemy
from sqlalchemy import (
    text,
)
# from ceonstock_db.models.base import Base

# Permissions setup following the advice of:
# https://vertabelo.com/blog/user-authentication-module/
# With SQLAlchemy's recommended implementation for mant-to-many relationships, using association tables:
# https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#many-to-many

# --------------------
# -- Mapping Tables --
# --------------------
# To create many:many relationships between entities we use a third table for mapping


# note for a Core table, we use the sqlalchemy.Column construct,
# not sqlalchemy.orm.mapped_column
class RolePermissionLinkTbl(SQLModel, table=True):
    __tablename__ = "granted_permission"

    role_id: UUID = Field(default=None, primary_key=True, foreign_key="role.id")
    permission_id: UUID = Field(
        default=None, primary_key=True, foreign_key="permission.id"
    )


# granted_permission_table = Table(
#     # Assigns permissions to user_roles
#     "granted_permission",
#     Base.metadata,
#     Column("role_uuid", ForeignKey("role.uuid"), primary_key=True),
#     Column("permission_uuid", ForeignKey("permission.uuid"), primary_key=True),
#     UniqueConstraint(  # Don't allow entries with the same user_role/permission combination
#         "role_uuid", "permission_uuid", name="_granted_permission_uc"
#     ),
# )


class UserRoleLinkTbl(SQLModel, table=True):
    __tablename__ = "granted_user_role"

    user_id: UUID = Field(default=None, primary_key=True, foreign_key="user.id")
    role_id: UUID = Field(default=None, primary_key=True, foreign_key="role.id")


# granted_user_role_table = Table(
#     "granted_user_role",
#     Base.metadata,
#     Column("user_id", ForeignKey("user.id"), primary_key=True),
#     Column("role_id", ForeignKey("role.id"), primary_key=True),
#     UniqueConstraint(  # Don't allow entries with the same account/role combination (no duplicate entries)
#         "user_uuid", "role_uuid", name="_granted_user_role_uc"
#     ),
# )


# --------------------
# -- Entity Tables --
# --------------------
# Lookup table
# A user role which can be assigned to a user to grant associated
# permissions.
class RoleTbl(SQLModel, table=True):
    __tablename__ = "role"

    id: UUID = Field(
        primary_key=True,
        default_factory=uuid4,
        sa_column_kwargs={
            "server_default": text("gen_random_uuid()"),
        },
    )
    name: str = Field(max_length=20, unique=True)
    description: str = Field(max_length=256, unique=False, nullable=True)
    permissions: list["PermissionTbl"] = Relationship(
        link_model=RolePermissionLinkTbl, back_populates="user_roles"
    )


# Lookup table
# Specific permissions which are checked for to perform an action
class PermissionTbl(SQLModel, table=True):
    __tablename__ = "permission"

    id: UUID = Field(
        primary_key=True,
        default_factory=uuid4,
        sa_column_kwargs={
            "server_default": text("gen_random_uuid()"),
        },
    )
    name: str = Field(max_length=30, unique=False)
    description: str = Field(max_length=256, nullable=True)
    user_roles: list["RoleTbl"] = Relationship(
        link_model=RolePermissionLinkTbl, back_populates="permissions"
    )
