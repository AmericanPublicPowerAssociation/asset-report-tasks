from asset_tracker.models import Asset
from asset_report_tasks.models.tasks import (
    Task, TaskStatus, TaskPriority)
from asset_report_tasks.views.tasks import (
    see_tasks_json, add_tasks_json, change_task_json)


class TestSeeTasksJson(object):

    def test_accept_parameters(self, website_request, db):
        db.add(Task(id='a', name='task a'))
        db.add(Task(id='b', name='task b'))
        db.add(Task(id='c', name='task b'))
        db.add(Task(id='d', name='task c'))
        website_response = see_tasks_json(website_request)
        assert 'tasks' in website_response
        assert len(website_response['tasks']) == 4
        assert website_response['tasks'][0]['id'] == 'a'
        assert website_response['tasks'][1]['id'] == 'b'
        assert website_response['tasks'][2]['id'] == 'c'
        assert website_response['tasks'][3]['id'] == 'd'


class TestAddTasksJson(object):

    def test_accept_parameters(self, website_request, db, mocker):
        db.add(Asset(id='asset-x'))
        task = Task(
            id='task-x',
            creation_user_id='u1',
            assignment_user_id='u2')
        mocker.patch(
            'asset_report_tasks.models.tasks.Task.make_unique_record',
            return_value=task)
        website_request.json_body = {
            'assetId': 'asset-x',
            'name': 'task a',
            'description': 'description a',
        }
        website_response = add_tasks_json(website_request)
        assert website_response['id'] == 'task-x'
        assert website_response['assetId'] == 'asset-x'
        assert website_response['name'] == 'task a'
        assert website_response['description'] == 'description a'
        assert website_response['status'] == TaskStatus.NEW.value
        assert website_response['priority'] == TaskPriority.NORMAL.value
        assert website_response['creationUserId'] == 'u1'
        assert website_response['assignmentUserId'] == 'u2'
        assert website_response['commentCount'] == 0


class TestChangeTaskJson(object):

    def test_accept_parameters(self, website_request, db):
        db.add(Task(id='task-x', name='task a', asset_id='asset-x'))
        website_request.json_body = {
            'name': 'task y',
            'status': TaskStatus.DONE.value,
            'priority': TaskPriority.LOW.value,
            'assignmentUserId': 'u2',
            'description': 'description b',
        }
        website_request.matchdict = {'task_id': 'task-x'}
        website_response = change_task_json(website_request)
        assert website_response['id'] == 'task-x'
        assert website_response['assetId'] == 'asset-x'
        assert website_response['name'] == 'task y'
        assert website_response['status'] == TaskStatus.DONE.value
        assert website_response['priority'] == TaskPriority.LOW.value
        assert website_response['assignmentUserId'] == 'u2'
        assert website_response['description'] == 'description b'


class TestDeleteTaskJson(object):
    pass
