import os
import sqlalchemy as sa
import logging


def create_engine(engine="sqlite:///:memory:", echo=False):
    logging.info(f"Creating Database Engine for {engine}")
    return sa.create_engine(os.getenv("DATABASE", engine), echo=echo)


def create_all_tables(Base, engine="sqlite:///:memory:"):
    Base.metadata.create_all(bind=engine)
    logging.info(f"Created all tables")
