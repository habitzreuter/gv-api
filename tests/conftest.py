"""
Configure pytest
"""
from unittest import mock
import pytest
from falcon import testing

import gv


@pytest.fixture
def mock_store():
    """
    Define a mock object to be returned by the database.
    This needs to be another fixture ir order to edit the database calls
    in the test functions.
    """
    return mock.MagicMock(autospec=True)

@pytest.fixture
def client(mock_store):
    """
    Generate a test client with fake database
    """
    # pylint: disable=protected-access,redefined-outer-name
    # This can be disabled because we need to call this protected
    # function in order to mock the database
    api = gv.create_app(mock_store)
    return testing.TestClient(api)
