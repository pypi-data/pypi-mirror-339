import logging
from sqlalchemy.orm import Session
from ceonstock_db import crud

from ceonstock_db.schemas import UserRoleOption
from ceonstock_db.schemas import PermissionOption

logger = logging.getLogger(__name__)
logger.setLevel("INFO")


GRANTED_PERMISSIONS = {
    UserRoleOption.VERIFIED_USER: [
        PermissionOption.SUBMIT_PREVIEWS,
        PermissionOption.PURCHASE,
    ],
    UserRoleOption.ADMIN: [permission for permission in PermissionOption],
}


def create_user_roles(session: Session):
    for user_role in UserRoleOption:
        logger.info(f"\tCreating user_role '{user_role}'")
        crud.access_control.create_role(session, user_role)


def create_permissions(session: Session):
    for permission in PermissionOption:
        logger.info(f"\tCreating permission '{permission}'")
        crud.access_control.create_permission(session, permission)


def assign_permissions_to_roles(session: Session):
    for role, permissions in GRANTED_PERMISSIONS.items():
        logger.info(f"\tCreating permission assignments for role '{role}':")
        for permission in permissions:
            crud.access_control.add_permission_to_role(session, role, permission)


def print_permissions(session):
    permissions_in_db = crud.access_control.get_all_permissions(session)
    logger.info(
        f"Found permissions in DB: {[permission_in_db.value for permission_in_db in permissions_in_db]}"
    )


def print_user_roles(session):
    roles_in_db = crud.access_control.get_all_user_roles(session)
    logger.info(
        f"Found roles in DB: {[role_in_db.value for role_in_db in roles_in_db]}"
    )


def push_to_db(session: Session):
    # TODO a way to UPDATE permissions, without a full DB reset.
    logger.info(GRANTED_PERMISSIONS)
    print()
    logger.info("-- Creating user_roles in db... --")
    create_user_roles(session)
    print()
    logger.info("-- Creating permission in db... --")
    create_permissions(session)

    # Assign permissions
    print()
    # TODO
    logger.info("-- Assigning permissions to roles in db... --")
    assign_permissions_to_roles(session)
