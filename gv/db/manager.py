"""
Database manager
"""
import os
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy.orm import scoping

from gv.db import models


class DBManager():
    """
    Database manager class.
    """
    def __init__(self, connection=None):
        if connection is None:
            db_path = os.path.join(os.getcwd(), 'db.sqlite3')
            self.connection = 'sqlite:///' + db_path
        else:
            self.connection = connection


        self.engine = sqlalchemy.create_engine(self.connection)
        self.db_session = scoping.scoped_session(
            orm.sessionmaker(
                bind=self.engine,
                autocommit=True
            )
        )

    @property
    def session(self):
        """
        Returns database session passed to API resources.
        """
        return self.db_session()

    def setup(self):
        """
        Setup database tables.
        """
        # pylint: disable=broad-except
        # This can be disabled because this is only setup code
        try:
            models.SAModel.metadata.create_all(self.engine)

        except Exception as exp:
            print('Could not initialize DB: {}'.format(exp))
