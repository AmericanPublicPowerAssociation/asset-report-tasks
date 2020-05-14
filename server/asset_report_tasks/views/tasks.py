from pyramid.httpexceptions import HTTPBadRequest, HTTPNotFound
from pyramid.view import view_config

from asset_tracker.models.asset import Asset
from asset_tracker.exceptions import DataValidationError

from ..models import Task, TaskStatus, TaskPriority
from ..routines import (get_task_priority_code, get_task_status_code,
                        get_enum_json_dictionary, get_viewable_tasks)


@view_config(
    route_name='tasks.json',
    renderer='json',
    request_method='GET')
def see_tasks_json(request):
    db = request.db
    # TODO: Get tasks for which user has view privileges
    tasks = get_viewable_tasks(db)
    return {
        'taskPriorityTypes': get_enum_json_dictionary(TaskPriority),
        'taskStatusTypes': get_enum_json_dictionary(TaskStatus),
        'tasks': [_.get_json_dictionary() for _ in tasks],
    }


@view_config(
    route_name='tasks.json',
    renderer='json',
    request_method='POST')
def add_tasks_json(request):
    db = request.db
    params = request.json_body
    try:
        asset_id = params['assetId']
        name = params['name']
        description = params['description']
        priority = get_task_priority_code(params)
        # TODO assigned task that links to risk
    except KeyError as e:
        raise HTTPBadRequest({e.args[0]: 'is invalid'})
    except DataValidationError as e:
        raise HTTPBadRequest(e.args[0])
    # Check whether asset_id exists
    asset_count = db.query(Asset).filter_by(id=asset_id).count()
    if not asset_count:
        raise HTTPBadRequest({'asset_id': 'is invalid'})
    task = Task.make_unique_record(db)
    task.name = name
    task.asset_id = asset_id
    task.description = description
    task.priority = priority
    db.add(task)
    db.flush()
    return task.get_json_dictionary()


@view_config(
    route_name='task.json',
    renderer='json',
    request_method='PATCH')
def change_task_json(request):
    db = request.db
    params = request.json_body
    task_id = request.matchdict['task_id']

    task = db.query(Task).get(task_id)
    if not task:
        raise HTTPNotFound
    if 'name' in params:
        task.name = params['name']
    if 'description' in params:
        task.description = params['description']
    if 'assignmentUserId' in params:
        task.assignment_user_id = params['assignmentUserId']
    try:
        task.status = get_task_status_code(params)
        task.priority = get_task_priority_code(params)
    except DataValidationError as e:
        raise HTTPBadRequest(e.args[0])
    db.add(task)
    db.flush()
    return task.get_json_dictionary()


'''
@view_config(
    route_name='task.json',
    renderer='json',
    request_method='DELETE')
def remove_task_json(request):
    db = request.db
    task_id = request.matchdict['task_id']
    task = db.query(Task).get(task_id)
    if not task:
        raise HTTPBadRequest('not valid params')  # HTTPNotFound
    # TODO delete task
    db.add(task)
    db.flush()
    return {}
'''
