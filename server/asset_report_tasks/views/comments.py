from pyramid.httpexceptions import HTTPBadRequest, HTTPNotFound
from pyramid.view import view_config

from ..models import Comment, Task


@view_config(
    route_name='task_comments.json',
    renderer='json',
    request_method='GET')
def see_comments_json(request):
    db = request.db
    task_id = request.matchdict['task_id']
    task = db.query(Task).get(task_id)
    if not task:
        raise HTTPNotFound
    # TODO: Check whether user has view access to task
    return [_.get_json_dictionary() for _ in task.comments]


@view_config(
    route_name='task_comments.json',
    renderer='json',
    request_method='POST')
def add_comment_json(request):
    db = request.db
    task_id = request.matchdict['task_id']
    params = request.json_body
    try:
        text = params['text']
    except KeyError as e:
        raise HTTPBadRequest({e.args[0]: 'is invalid'})
    task = db.query(Task).get(task_id)
    if not task:
        raise HTTPNotFound
    comment = Comment.make_unique_record(db)
    comment.text = text
    comment.task_id = task_id
    db.add(comment)
    db.flush()
    return comment.get_json_dictionary()


@view_config(
    route_name='task_comment.json',
    renderer='json',
    request_method='PATCH')
def change_comment_json(request):
    db = request.db
    task_id = request.matchdict['task_id']
    comment_id = request.matchdict['comment_id']
    params = request.json_body
    try:
        text = params['text']
    except KeyError as e:
        raise HTTPBadRequest({e.args[0]: 'is invalid'})
    task = db.query(Task).get(task_id)
    comment = db.query(Comment).get(comment_id)
    if not task:
        raise HTTPNotFound({'task_id': 'does not exist'})
    if not comment:
        raise HTTPNotFound({'comment_id': 'does not exist'})
    comment.text = text
    db.add(comment)
    db.flush()
    return comment.get_json_dictionary()


'''
@view_config(
    route_name='task_comment.json',
    renderer='json',
    request_method='DELETE')
def remove_comment_json(request):
    pass
'''
