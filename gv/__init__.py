"""
GV API
"""
import falcon

from gv import tasks
from gv.db.manager import DBManager


def create_app(db_manager):
    """
    Creates app instance

    This should be called by the get_app, where the dependencies will
    be configured. Only tests should call this function directly because
    they use mocks instead of get_app
    """
    api = falcon.API()

    # Create Resources
    task_list = tasks.Collection(db_manager)
    task_item = tasks.Item(db_manager)

    # Define routes
    api.add_route('/tasks', task_list)
    api.add_route('/tasks/{task_id:int}', task_item)

    return api

def get_app():
    """
    Configures app instance and it's dependencies
    """

    # Configuration
    db_manager = DBManager()
    db_manager.setup()

    return create_app(db_manager)
