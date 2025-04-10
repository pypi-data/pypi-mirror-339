from uuid import uuid4, UUID

from sqlmodel import SQLModel, Field

from sqlalchemy import (
    text,
)

# Information about goods that can be ordered.


class ProductTbl(SQLModel, table=True):
    __tablename__ = "product"

    id: UUID = Field(
        primary_key=True,
        index=True,
        default_factory=uuid4,
        sa_column_kwargs={"server_default": text("gen_random_uuid()")},
    )
    name: str = Field(max_length=30, nullable=False)
    description: str = Field(max_length=250, nullable=False)
    price_gbp_pence: int = Field(nullable=False)
