"""
Database models
"""

import enum
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.inspection import inspect


SAModel = declarative_base()

class Status(enum.Enum):
    """
    Enumeration for task status.
    """
    TODO = 0
    READY = 1
    DONE = 2
    MISSED = 3

class Group(enum.Enum):
    """
    Enumeration for task group.
    """
    RIDDLE = 0
    MEDIA = 1
    ARTS = 2
    SEARCH = 3
    SPORTS = 4
    selfECT = 5
    MISC = 6
    OTHER = 7

class Task(SAModel):
    """
    Task model.
    """
    __tablename__ = 'tasks'

    id = sa.Column(sa.Integer, primary_key=True)
    number = sa.Column(sa.Integer)
    title = sa.Column(sa.String(100))
    due_date = sa.Column(sa.String(30))
    created = sa.Column(sa.String(30))
    modified = sa.Column(sa.String(30))
    location = sa.Column(sa.String(30))
    assigned_to = sa.Column(sa.String(100))
    status = sa.Column(sa.Enum(Status))
    group = sa.Column(sa.Enum(Group))
    score = sa.Column(sa.Integer)
    max_score = sa.Column(sa.Integer)
    extra_info = sa.Column(sa.String(512))
    url = sa.Column(sa.String(256))
    active = sa.Column(sa.Boolean)

    @property
    def serialize(self):
        """
        Return object data in easily serializeable format.
        """
        task = {}
        for item in inspect(self).attrs.keys():
            prop = getattr(self, item)
            if isinstance(prop, enum.Enum):
                task[item] = prop.name
            else:
                task[item] = prop
        return task


    @classmethod
    def get_all(cls, session):
        """
        Get all tasks from database.
        """
        tasks = []

        with session.begin():
            query = session.query(cls)
            tasks = query.all()

        return tasks

    @classmethod
    def get(cls, session, task_id):
        """
        Get task with given id.
        """
        task = {}

        with session.begin():
            query = session.query(cls)
            task = query.get(task_id)

        return task
