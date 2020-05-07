from asset_report_tasks.models.comments import Comment
from asset_report_tasks.models.tasks import Task
from asset_report_tasks.views.comments import (
    see_comments_json, add_comment_json, change_comment_json)


class TestSeeCommentsJson(object):

    def test_accept_parameters(self, website_request, db):
        db.add(Task(id='task-x'))
        db.add(Comment(id='comment 1', task_id='task-x'))
        db.add(Comment(id='comment 2', task_id='task-x'))
        db.add(Comment(id='comment 3'))
        db.add(Comment(id='comment 4'))
        website_request.matchdict = {'task_id': 'task-x'}
        website_response = see_comments_json(website_request)
        assert len(website_response) == 2
        assert website_response[0]['id'] == 'comment 1'
        assert website_response[1]['id'] == 'comment 2'
        assert website_response[0]['taskId'] == 'task-x'
        assert website_response[1]['taskId'] == 'task-x'


class TestAddCommentsJson(object):

    def test_accept_parameters(self, website_request, db, mocker):
        db.add(Task(id='task-x'))
        website_request.matchdict = {'task_id': 'task-x'}
        comment = Comment(id='comment-x')
        website_request.json_body = {
            'text': 'comment 1',
        }
        mocker.patch(
            'asset_report_tasks.models.comments.Comment.make_unique_record',
            return_value=comment
        )
        website_response = add_comment_json(website_request)
        assert website_response['id'] == 'comment-x'
        assert website_response['taskId'] == 'task-x'
        assert website_response['text'] == 'comment 1'
        # assert website_response['creationTimestamp'] == ''
        # assert website_response['modificationTimestamp'] == ''
        # assert website_response['creationUserId'] == ''


class TestChangeCommentsJson(object):

    def test_accept_parameters(self, website_request, db):
        db.add(Task(id='task-x'))
        db.add(Comment(id='commentX', task_id='task-x'))
        website_request.matchdict = {
            'comment_id': 'commentX',
            'task_id': 'task-x',
        }
        website_request.json_body = {
            'text': 'change comment 1',
        }
        website_response = change_comment_json(website_request)
        assert website_response['id'] == 'commentX'
        assert website_response['taskId'] == 'task-x'
        assert website_response['text'] == 'change comment 1'
        # assert website_response['creationTimestamp'] == ''
        # assert website_response['modificationTimestamp'] == ''
        # assert website_response['creationUserId'] == ''
