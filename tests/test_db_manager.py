"""
Test DBManager class
"""
# pylint: disable=missing-docstring
import os
from gv.db.manager import DBManager


def test_connection_automatic_path():
    database = DBManager()

    assert 'sqlite:///' in database.connection
    assert 'db.sqlite3' in database.connection
    assert os.getcwd() in database.connection

def test_connection_path():
    database = DBManager('sqlite:////hello')

    assert 'sqlite:////hello' in database.connection
