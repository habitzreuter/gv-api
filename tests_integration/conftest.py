"""
Configure pytest
"""
import os
import tempfile
import pytest
from falcon import testing

import gv
from gv.db.manager import DBManager


@pytest.fixture
def client():
    """
    Generate a test client with temp database for integration testing
    Based on http://flask.pocoo.org/docs/1.0/tutorial/tests/
    """
    # pylint: disable=protected-access,redefined-outer-name
    # This can be disabled because we need to call this protected
    # function in order to mock the database

    db_fd, db_path = tempfile.mkstemp()

    db_manager = DBManager('sqlite:///' + db_path)
    db_manager.setup()

    api = gv.create_app(db_manager)

    yield testing.TestClient(api)

    os.close(db_fd)
    os.unlink(db_path)
