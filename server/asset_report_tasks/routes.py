def includeme(config):
    config.add_route(
        'tasks.json',
        '/tasks.json')
    config.add_route(
        'task.json',
        '/tasks/{task_id}.json')
    config.add_route(
        'task_comments.json',
        '/tasks/{task_id}/comments.json')
    config.add_route(
        'task_comment.json',
        '/tasks/{task_id}/comments/{comment_id}.json')
