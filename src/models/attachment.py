from sqlalchemy import String, Column, DateTime, Text, ForeignKey
from src.database import db
from sqlalchemy.dialects.postgresql import JSON
from src.utils import get_current_time, generate_unique_key
from .stage import Stage
from .project import Project
from .task import Task


class Attachment(db.Model):
    __tablename__ = "attachments"

    attachment_id = Column(String(22), primary_key=True, default=generate_unique_key)
    project_id = Column(String, ForeignKey(Project.project_id, ondelete="CASCADE"))
    stage_id = Column(String, ForeignKey(Stage.stage_id, ondelete="CASCADE"))
    task_id = Column(String, ForeignKey(Task.task_id, ondelete="CASCADE"))
    subtask_id = Column(String)
    file_name = Column(String)
    file_type = Column(String)
    file_data = Column(JSON)
    created_at = Column(DateTime(timezone=True), default=get_current_time)

    def get_details(self):
        return {
            "attachment_id": self.attachment_id,
            "project_id": self.project_id,
            "stage_id": self.stage_id,
            "task_id": self.task_id,
            "subtask_id": self.subtask_id,
            "file_name": self.file_name,
            "file_type": self.file_type,
            "file_data": self.file_data,
            "created_at": self.created_at,
        }
