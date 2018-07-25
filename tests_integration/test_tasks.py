# pylint: disable=no-member,missing-docstring
import json
import falcon


def test_create_get_tasks(client):
    task = {
        'number': 3,
        'title': 'Hello',
    }

    res1 = client.simulate_post('/tasks/', body=json.dumps(task))
    assert res1.status == falcon.HTTP_CREATED

    res2 = client.simulate_get('/tasks/')
    assert res2.status == falcon.HTTP_OK
    assert b'"number": 3, "title": "Hello"' in res2.content

def test_create_get_task(client):
    task = {
        'number': 3,
        'title': 'Hello',
    }

    res1 = client.simulate_post('/tasks/', body=json.dumps(task))
    assert res1.status == falcon.HTTP_CREATED

    res2 = client.simulate_get('/tasks/1')
    assert res2.status == falcon.HTTP_OK
    assert b'"number": 3, "title": "Hello"' in res2.content

def test_create_task_bad_request(client):
    task = {
        'number': 'abc',
        'title': 'Hello',
    }

    res1 = client.simulate_post('/tasks/', body=json.dumps(task))
    assert res1.status == falcon.HTTP_BAD_REQUEST

    res2 = client.simulate_get('/tasks/')
    assert res2.status == falcon.HTTP_OK
    assert b'' in res2.content

def test_user_cant_change_id(client):
    task = {
        'id': 4,
    }

    res1 = client.simulate_post('/tasks/', body=json.dumps(task))
    assert res1.status == falcon.HTTP_CREATED

    res2 = client.simulate_get('/tasks/')
    assert res2.status == falcon.HTTP_OK
    assert b'"id": 1, "number"' in res2.content

def test_create_update_task(client):
    task = {
        'number': 3,
        'title': 'Hello',
    }

    res1 = client.simulate_post('/tasks/', body=json.dumps(task))
    assert res1.status == falcon.HTTP_CREATED

    res2 = client.simulate_get('/tasks/')
    assert res2.status == falcon.HTTP_OK
    assert b'"number": 3, "title": "Hello"' in res2.content

    task_id = json.loads(res2.content)[0]['id']

    task['number'] = 7

    res3 = client.simulate_put(
        '/tasks/{}'.format(task_id),
        body=json.dumps(task)
    )
    assert res3.status == falcon.HTTP_OK

    res4 = client.simulate_get('/tasks/{}'.format(task_id))
    assert res4.status == falcon.HTTP_OK
    assert b'"number": 7, "title": "Hello"' in res4.content

def test_create_delete_task(client):
    task = {
        'number': 3,
        'title': 'Hello',
    }

    res1 = client.simulate_post('/tasks/', body=json.dumps(task))
    assert res1.status == falcon.HTTP_CREATED

    res2 = client.simulate_get('/tasks/')
    assert res2.status == falcon.HTTP_OK
    assert b'"number": 3, "title": "Hello"' in res2.content

    task_id = json.loads(res2.content)[0]['id']

    res3 = client.simulate_delete('/tasks/{}'.format(task_id))
    assert res3.status == falcon.HTTP_OK

    res4 = client.simulate_get('/tasks/{}'.format(task_id))
    assert res4.status == falcon.HTTP_NOT_FOUND
    assert b'' in res4.content

    res5 = client.simulate_get('/tasks/')
    assert res5.status == falcon.HTTP_OK
    assert b'[]' in res5.content
