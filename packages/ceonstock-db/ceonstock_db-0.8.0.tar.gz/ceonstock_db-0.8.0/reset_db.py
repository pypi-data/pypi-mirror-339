import os
import logging
import dotenv

from ceonstock_db import database
import db_setup_scripts

dotenv.load_dotenv("./.env")

root_logger = logging.getLogger()
root_logger.setLevel("DEBUG")

logger = logging.getLogger(__name__)


def main():
    DB_URI = os.getenv("DB_URI")
    print(f"Got DB_URI: {DB_URI}")
    if not DB_URI:
        raise Exception("Did not receive a DB_URI")
    # For local dev, disable ssl require
    print(f"WARNING: You are about to reset the DB at:")
    print(f"\t{DB_URI}")

    if not confirm_user_intent("Continue?"):
        print("Exiting.")
        return

    connect_args_dev = {}
    session_maker = database.create_local_session_maker(
        DB_URI, connect_args=connect_args_dev
    )
    with session_maker() as session:
        db_setup_scripts.reset.reset_schema(session)
        print(f"Database has been reset and rebuilt with the latest schema.")

        print(f"Populating default data (user roles)")
        # Populate with fundamental/required data such as user roles
        setup_default_state(session)

        # Populate with default data
        # if confirm_user_intent(f"Populate database with default data?"):
        #     setup_default_entries(session)


def setup_default_state(session):
    """
    State which is assumed to always be desired as setup
        - Access control (user roles and assigned permissions)
    """
    db_setup_scripts.access_control.push_to_db(session)
    db_setup_scripts.products.create_default_products(session)


def setup_default_entries(session):
    """
    Default database entries that may or may not be desired.
        - Users
        - Projects
    """
    db_setup_scripts.users.create_default_users(session)


def confirm_user_intent(msg: str):
    user_resp = input(f"{msg} ('yes' to continue): ")
    if user_resp.lower() == "yes":
        return True
    return False


if __name__ == "__main__":
    main()
