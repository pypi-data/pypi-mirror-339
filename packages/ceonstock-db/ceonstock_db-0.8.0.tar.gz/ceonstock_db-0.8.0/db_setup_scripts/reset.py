import logging

import sqlalchemy
from sqlalchemy.orm import Session

from sqlmodel import SQLModel

# Importing the models also means that all of the classes
# which inherit from base are imported (via __init__.py)
# This is necessary for the tables to register their metadata.

# Setup logger
logger = logging.getLogger(__name__)
logger.setLevel("INFO")


def get_live_metadata(session: Session):
    """Get the metadata from the live DB via the engine connection"""
    engine = session.get_bind()
    # Create empty metadata
    live_metadata = sqlalchemy.schema.MetaData()
    # Popoulate it with data from the db
    live_metadata.reflect(bind=engine)
    return live_metadata


def get_python_metadata():
    """
    Returns the metadata as defined by local python modules inheriting from the base class
    Note that classes must have been imported to be 'loaded'
        from ceonstock_db import models <-- imported classes via __init__.py
    """
    # return models.base.Base.metadata
    return SQLModel.metadata


def clear_data(session: Session):
    logger.warning(f"Clearing all entries in db...")
    live_metadata = get_live_metadata(session)
    for table in reversed(live_metadata.sorted_tables):
        logger.info(f"Removing all entries in table: {table}")
        session.execute(table.delete())
    session.commit()


def print_live_tables(session: Session):
    # Get the metadata from the live DB
    live_metadata = get_live_metadata(session)
    if not live_metadata.tables:
        logger.info(f"\t(None found)")
        return
    for table in live_metadata.tables:
        logger.info(f"\t{table}")


def clear_tables(session):
    """Drop all tables in the DB"""
    logger.warning(f"Dropping all tables in db...")
    live_metadata = get_live_metadata(session)
    engine = session.get_bind()
    live_metadata.drop_all(bind=engine)


def create_tables(session):
    """Load the tables into the live DB as defined by our sqlalchemy models"""
    logger.info("Creating tables...")
    engine = session.get_bind()
    metadata = get_python_metadata()
    metadata.create_all(bind=engine)
    print_live_tables(session)


def reset_schema(session):
    logger.warning(
        "Resetting schema (Dropping all tables and data) and recreating tables..."
    )
    clear_tables(session)
    create_tables(session)
