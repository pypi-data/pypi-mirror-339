from uuid import UUID

from sqlmodel import SQLModel, Field

# from ceonstock_db.models.base import Base


class UserStripeTbl(SQLModel, table=True):
    # Map an app user to their stripe customer id.
    __tablename__ = "user_stripe"

    user_account_id: UUID = Field(
        foreign_key="user.id",
        ondelete="CASCADE",
        primary_key=True,
    )
    stripe_customer_id: str = Field(max_length=30, unique=True)
