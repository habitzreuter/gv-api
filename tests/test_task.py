# pylint: disable=no-member,missing-docstring
# No need for documentation in tests
import json
from unittest.mock import ANY
import falcon

from gv.db.models import Task

def test_get_task_list(client, mock_store):

    task1 = Task(id=1, number=3, title='Creative title')
    task2 = Task(id=0, number=4, title='Creative title 2')
    mock_store.session.query().all.return_value = [task1, task2]

    res = client.simulate_get('/tasks/')

    mock_store.session.query().all.assert_called_once()
    assert res.status == falcon.HTTP_OK
    assert b'{"id": 1, "number": 3, "title": "Creative title"' in res.content
    assert b'{"id": 0, "number": 4, "title": "Creative title 2"' in res.content

def test_get_single_task(client, mock_store):
    task_id = 2
    task = Task(id=task_id, number=3)
    mock_store.session.query().get.return_value = task

    res = client.simulate_get('/tasks/{}'.format(task_id))

    mock_store.session.query().get.assert_called_once_with(task_id)
    assert res.status == falcon.HTTP_OK
    assert '{{"id": {}, "number": 3'.format(task_id) in str(res.content)

def test_get_single_task_not_found(client, mock_store):
    task_id = 2
    mock_store.session.query().get.return_value = None

    res = client.simulate_get('/tasks/{}'.format(task_id))
    mock_store.session.query().get.assert_called_once_with(task_id)
    assert res.status == falcon.HTTP_NOT_FOUND

def test_create_task(client, mock_store):

    task = {
        'number': 3,
        'title': 'Hello',
        'due_date': '2013-03-25T12:42:31+00:32',
        'some_weird_field': 3,
        'status': 'DONE'
    }

    response = client.simulate_post('/tasks/', body=json.dumps(task))

    assert response.status == falcon.HTTP_CREATED
    mock_store.session.add.assert_called_once_with(ANY)

def test_create_task_invalid_date(client, mock_store):

    task = {
        'number': 3,
        'title': 'Hello',
        'due_date': '2013-3-25T12:42:31+00:32',
    }

    response = client.simulate_post('/tasks/', body=json.dumps(task))

    assert response.status == falcon.HTTP_BAD_REQUEST
    mock_store.session.add.assert_not_called()

def test_create_task_invalid_number(client, mock_store):

    task = {
        'number': 'string',
        'title': 'Hello',
    }

    response = client.simulate_post('/tasks/', body=json.dumps(task))

    assert response.status == falcon.HTTP_BAD_REQUEST
    mock_store.session.add.assert_not_called()

def test_create_task_invalid_url(client, mock_store):

    task = {
        'number': 3,
        'title': 'Hello',
        'url': '^]ḉ'
    }

    response = client.simulate_post('/tasks/', body=json.dumps(task))

    assert response.status == falcon.HTTP_BAD_REQUEST
    mock_store.session.add.assert_not_called()

def test_create_task_server_error(client, mock_store):

    mock_store.session.add.side_effect = Exception('Test Exception')

    task = {
        'number': 3,
        'title': 'Hello',
        'due_date': '2013-03-25T12:42:31+00:32',
    }

    response = client.simulate_post('/tasks/', body=json.dumps(task))

    assert response.status == falcon.HTTP_INTERNAL_SERVER_ERROR
    assert b'Test Exception' in response.content


def test_update_task(client, mock_store):

    old_task_data = {
        'id': 1,
        'number': 11,
    }

    new_task_data = {
        'number': 3,
        'title': 'Hello',
        'due_date': '2013-03-25T12:42:31+00:32',
    }


    old_task = Task(
        id=old_task_data['id'],
        number=old_task_data['number']
    )

    mock_store.session.query().get.return_value = old_task

    def side_effect(self):
        assert self.id == old_task_data['id']
        assert self.number == new_task_data['number']
        assert self.due_date == new_task_data['due_date']

    mock_store.session.merge.side_effect = side_effect

    response = client.simulate_put(
        '/tasks/' + str(old_task_data['id']),
        body=json.dumps(new_task_data)
    )

    assert response.status == falcon.HTTP_OK

def test_update_task_not_found(client, mock_store):
    new_task_data = {
        'number': 3,
        'title': 'Hello',
        'due_date': '2013-03-25T12:42:31+00:32',
    }

    mock_store.session.query().get.return_value = None

    response = client.simulate_put('/tasks/1', body=json.dumps(new_task_data))

    mock_store.session.merge.assert_not_called()
    mock_store.session.query().get.assert_called_once_with(1)
    assert response.status == falcon.HTTP_NOT_FOUND
