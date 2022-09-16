import logging
from contextlib import contextmanager

import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.ddl import CreateSchema

from backend import settings

settings = settings.Settings()
logger = logging.getLogger(__name__)
Session = sessionmaker(autocommit=False)


class DatabaseCon:
    """
    A database connection object. Contains a context manager to load database sessions.
    """

    def __init__(self):
        logger.info("Connecting to database")
        self.SCHEMA_NAME = "grow"
        self.engine = sqlalchemy.create_engine(
            settings.db_url(),
            pool_size=10,
            max_overflow=0,
            connect_args={"connect_timeout": 5},
        )
        conn = self.engine.connect()
        if not conn.dialect.has_schema(conn, self.SCHEMA_NAME):
            logger.info("Creating database schema")
            conn.execute(CreateSchema(self.SCHEMA_NAME))

        Session.configure(bind=self.engine)
        self.session = Session()

    @contextmanager
    def get_db_session(self):
        try:
            yield self.session
        except Exception as e:
            self.session.rollback()
            logger.error(e)
            raise
        finally:
            self.session.close()


db = DatabaseCon()
