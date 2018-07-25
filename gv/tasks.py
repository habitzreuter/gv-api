"""
GV API
Handle task manipulation
"""
import json
import datetime
import falcon
from falcon.media.validators import jsonschema

from gv.schema.task import SCHEMA as task_schema
from gv.db import models


class Collection():
    """
    Handle stuff related to multiple tasks
    """
    # pylint: disable=too-few-public-methods
    # This pylint warning can be disable because falcon requires
    # a class, so this is the only way to do it
    def __init__(self, db):
        self._db = db

    def on_get(self, req, resp):
        """
        Returns all tasks in the database
        """
        # pylint: disable=unused-argument
        model_list = models.Task.get_all(self._db.session)
        tasks = []
        for task in model_list:
            tasks.append(task.serialize)

        resp.body = json.dumps(tasks)

    @jsonschema.validate(task_schema)
    def on_post(self, req, resp):
        """
        Create a new task in the database
        """

        # Extract task fields from request
        # Only fields that can be changed by the user should be here
        model = models.Task(
            title=req.media.get('title'),
            number=req.media.get('number'),
            status=req.media.get('status'),
            group=req.media.get('group'),
            score=req.media.get('score'),
            max_score=req.media.get('max_score'),
            extra_info=req.media.get('extra_info'),
            assigned_to=req.media.get('assigned_to'),
            url=req.media.get('url'),
            due_date=req.media.get('due_date'),
            location=req.media.get('location'),
        )

        # Initialize fields with sane values
        now = datetime.datetime.now()
        model.created = now
        model.modified = now

        model.active = True

        if model.status is None:
            model.status = 'TODO'

        try:
            model.save(self._db.session)
        except Exception as exp:
            raise falcon.HTTPInternalServerError(description=str(exp))

        resp.status = falcon.HTTP_CREATED

class Item():
    """
    Handle stuff related to a single task
    """
    # pylint: disable=too-few-public-methods
    # This pylint warning can be disable because falcon requires
    # a class, so this is the only way to do it
    def __init__(self, db):
        self._db = db

    def on_get(self, req, resp, task_id):
        """
        Return task with the given id
        """
        # pylint: disable=unused-argument
        task = models.Task.get(self._db.session, task_id)

        if task is not None:
            resp.body = json.dumps(task.serialize)
            return

        resp.status = falcon.HTTP_NOT_FOUND

    @jsonschema.validate(task_schema)
    def on_put(self, req, resp, task_id):
        """
        Update task with the given id
        """
        task = models.Task.get(self._db.session, task_id)
        if task is None:
            resp.status = falcon.HTTP_NOT_FOUND
            return

        new_task = models.Task(
            title=req.media.get('title'),
            number=req.media.get('number'),
            status=req.media.get('status'),
            group=req.media.get('group'),
            score=req.media.get('score'),
            max_score=req.media.get('max_score'),
            extra_info=req.media.get('extra_info'),
            assigned_to=req.media.get('assigned_to'),
            url=req.media.get('url'),
            due_date=req.media.get('due_date'),
            location=req.media.get('location'),
        )

        new_task.id = task.id
        new_task.created = task.created

        now = datetime.datetime.now()
        new_task.modified = now

        new_task.update(self._db.session)

    def on_delete(self, req, resp, task_id):
        """
        Delete task with the given id
        """
        # pylint: disable=unused-argument
        task = models.Task.get(self._db.session, task_id)
        if task is None:
            resp.status = falcon.HTTP_NOT_FOUND
            return

        now = datetime.datetime.now()
        task.modified = now

        task.delete(self._db.session)
