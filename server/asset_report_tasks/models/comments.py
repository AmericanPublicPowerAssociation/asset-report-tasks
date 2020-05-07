from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import (
    String, UnicodeText)
from asset_tracker.models.meta import (
    Base, ModificationMixin, CreationMixin, RecordMixin)


class Comment(ModificationMixin, CreationMixin, RecordMixin, Base):
    __tablename__ = 'comment'
    text = Column(UnicodeText)
    creation_user_id = Column(String)
    task_id = Column(String, ForeignKey('task.id'))
    task = relationship('Task', backref='comments')

    def get_json_dictionary(self):
        return {
            'id': self.id,
            'text': self.text,
            'taskId': self.task_id,
            'creationUserId': self.creation_user_id,
            'modificationTimestamp': self.creation_datetime.timestamp(),
            'creationTimestamp': self.modification_datetime.timestamp(),
        }
