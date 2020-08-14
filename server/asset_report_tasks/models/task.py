import enum
from appa_auth_consumer.constants import ROLE_SPECTATOR
from asset_tracker.models import Asset
from asset_tracker.routines import get_utility_ids
from invisibleroads_records.models import (
    Base,
    ModificationMixin,
    CreationMixin,
    RecordMixin)
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import (
    String, Unicode, Enum)


class TaskStatus(enum.Enum):
    CANCELLED = -1
    NEW = 0
    PENDING = 10
    DONE = 100


class TaskPriority(enum.Enum):
    NORMAL = 10
    IMPORTANT = 100


class Task(ModificationMixin, CreationMixin, RecordMixin, Base):
    __tablename__ = 'task'
    name = Column(Unicode)
    status = Column(Enum(TaskStatus), default=TaskStatus.NEW)
    priority = Column(Enum(TaskPriority), default=TaskPriority.NORMAL)
    description = Column(Unicode)
    assignment_user_id = Column(String)  # only one user assigned
    creation_user_id = Column(String)
    asset_id = Column(String, ForeignKey('asset.id'))
    asset = relationship('Asset', backref='tasks')
    # comments = relationship('Comment', backref='task')
    reference_uri = Column(String)

    @classmethod
    def get_viewable_query(Class, request):
        db = request.db
        session = request.session
        utility_ids = get_utility_ids(session, ROLE_SPECTATOR)
        query = db.query(Class).join(Task.asset).filter(
            Asset.utility_id.in_(utility_ids),
            Asset.is_deleted == False)  # noqa: E712
        return query

    def get_json_dictionary(self):
        return {
            'id': self.id,
            'name': self.name,
            'status': self.status.value,
            'priority': self.priority.value,
            'description': self.description,
            'assignmentUserId': self.assignment_user_id,
            'creationUserId': self.creation_user_id,
            'assetId': self.asset_id,
            'commentCount': len(self.comments),
        }
