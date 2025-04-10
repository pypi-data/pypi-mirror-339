from uuid import uuid4, UUID
from datetime import datetime

from sqlmodel import SQLModel, Field

from sqlalchemy import func, text

# Tables for tracking a user's order.


class OrderTbl(SQLModel, table=True):
    __tablename__ = "order"

    id: UUID = Field(
        primary_key=True,
        index=True,
        default_factory=uuid4,
        sa_column_kwargs={"server_default": text("gen_random_uuid()")},
    )
    user_account_id: UUID
    # No foreign key since products could potentially be deleted but we'd want to maintain the order record.
    product_id: UUID
    created_at: datetime = Field(sa_column_kwargs={"server_default": func.now()})
    updated_at: datetime = Field(
        sa_column_kwargs={"server_default": func.now(), "onupdate": func.now()}
    )
    # PENDING (Awaiting payment), RECEIVED, COMPLETE, CANCELLED, REFUNDED
    order_status: str = Field(max_length=30, nullable=False)


# TODO implment into system
# class OrderExpenseTbl(SQLModel, table=True):
#     # Track expenses created while fulfilling an order.
#     __tablename__ = "order_expense"

#     id: UUID = Field(
#         UUID(as_uuid=True),
#         primary_key=True,
#         default=uuid4,
#         server_default=text("gen_random_uuid()"),
#         unique=True,
#         nullable=False,
#         index=True,
#     )
#     order_id: UUID = Field(
#         UUID(as_uuid=True),
#         ForeignKey("order.id"),
#     )
#     # Category e.g. 'rendering', 'file_storage', 'payment_processing', 'affiliate_payment'
#     expense_type: str = Field(String(30), nullable=False)
#     # Specific info e.g. 'stripe fees' or '300 credits via Conductor' or 'Project files (12.2gb) stored since 01/01/2024'
#     expense_description: str = Field(String(200), nullable=False)


# TODO implement into system
# class OrderRevenueTbl(SQLModel, table=True):
#     # Track sources of revenue related to this order,
#     # or if the order was payed for with credits/tokens?
#     __tablename__ = "order_payment"

#     id: UUID = Field(
#         UUID(as_uuid=True),
#         primary_key=True,
#         default=uuid4,
#         server_default=text("gen_random_uuid()"),
#         unique=True,
#         nullable=False,
#         index=True,
#     )
#     order_id: UUID = Field(
#         UUID(as_uuid=True),
#         ForeignKey("order.id"),
#         primary_key=True,
#     )
#     # Stripe / other
#     payment_provider: str = Field(String(30))
