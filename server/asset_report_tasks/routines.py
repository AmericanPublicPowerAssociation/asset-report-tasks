from asset_tracker.exceptions import DataValidationError

from .models import TaskPriority, TaskStatus


def get_task_priority_code(task_dictionary):
    try:
        task_priority_code = task_dictionary['priority']
    except KeyError:
        raise DataValidationError({'priority': 'is required'})

    try:
        task_priority_code = TaskPriority(task_priority_code)
    except ValueError:
        raise DataValidationError({'priority': 'is invalid'})
    return task_priority_code


def get_task_status_code(task_dictionary):
    try:
        task_status_code = task_dictionary['status']
    except KeyError:
        raise DataValidationError({'status': 'is required'})

    try:
        task_status_code = TaskStatus(task_status_code)
    except ValueError:
        raise DataValidationError({'status': 'is invalid'})
    return task_status_code


def get_enum_json_dictionary(enum):
    arr = []
    for e in enum:
        arr.append({
            'name': e.name.capitalize(),
            'code': e.value,
        })
    return arr
