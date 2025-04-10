import logging
from typing import Optional
from sqlalchemy.orm import Session
from ceonstock_db import schemas
from ceonstock_db import crud
from ceonstock_db.schemas import UserRoleOption

logger = logging.getLogger(__name__)


class DefaultUser:
    def __init__(
        self,
        user_create: schemas.UserAccountCreate,
        roles: Optional[list[UserRoleOption]] = None,
    ):
        self.user_account = user_create
        self.roles = roles


# TODO for a more consistent workflow, replace with pydantic creation classes similar to
# what the API user will be working with.
DEFAULT_USERS = [
    DefaultUser(
        schemas.UserAccountCreate(
            email="admin@ceonstock.com",
            password="123",
            profile=schemas.UserProfileCreate(
                username="CeonStock", first_name="Dayne", last_name="Kolk"
            ),
        ),
        [UserRoleOption.ADMIN],
    ),
    DefaultUser(
        schemas.UserAccountCreate(email="daynekolk@hotmail.com", password="123")
    ),
]


def create_default_user(session: Session, user_to_create: DefaultUser):
    new_user = crud.user.create(session, user_to_create.user_account)
    logger.debug(f"Created new user: {new_user.email}")
    if user_to_create.roles:
        logger.warning(
            f"Assigning roles to user {new_user.email}: {user_to_create.roles}"
        )
        for role in user_to_create.roles:
            crud.access_control.add_role_to_user(
                session, user_account=new_user, role_to_add=role
            )
    session.commit()


def create_default_users(session: Session):
    for default_user in DEFAULT_USERS:
        create_default_user(session, default_user)


def create_admin_user(session: Session):
    # TODO setup admin with env vars
    raise NotImplementedError
