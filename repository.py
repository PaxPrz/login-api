import os
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from helpers import create_engine


engine = create_engine(os.getenv("DATABASE"))

class SqlSession:
    def __init__(self, engine):
        self._Session = sessionmaker(bind=engine)
        self.session = self._Session()

    def __enter__(self):
        return self.session

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_type is None:
            self.session.commit()
            return True
        self.session.rollback()
