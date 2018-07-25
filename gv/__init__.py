"""
GV API
"""
import falcon

from gv import tasks
from gv.db.manager import DBManager


class CORSMiddleware:
    def process_request(self, req, resp):
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Headers', 'content-type')
        resp.set_header('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')

def create_app(db_manager):
    """
    Creates app instance

    This should be called by the get_app, where the dependencies will
    be configured. Only tests should call this function directly because
    they use mocks instead of get_app
    """
    api = falcon.API(middleware=[CORSMiddleware()])

    # Create Resources
    task_list = tasks.Collection(db_manager)
    task_item = tasks.Item(db_manager)

    # Define routes
    api.add_route('/tasks', task_list)
    api.add_route('/tasks/{task_id:int}', task_item)
    api.add_route('/task/{task_id:int}', task_item)

    return api

def get_app():
    """
    Configures app instance and it's dependencies
    """

    # Configuration
    db_manager = DBManager()
    db_manager.setup()

    return create_app(db_manager)
