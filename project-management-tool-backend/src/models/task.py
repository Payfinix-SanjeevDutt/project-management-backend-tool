from sqlalchemy import String, Column, DateTime, Text ,ForeignKey
from src.database import db
from src.utils import get_current_time, generate_unique_key
from .stage import Stage
from .sprint import Sprint

class Priorities:

    LOW = 'LOW'
    HIGH = 'HIGH'
    MEDIUM = 'MEDIUM'
    CRITICAL = 'CRITICAL'


class TaskStatus:

    TODO = 'TODO'
    IN_PROGRESS = 'IN_PROGRESS'
    DONE = 'DONE'


class Task(db.Model):
    __tablename__ = "tasks"

    task_id = Column(String(22), primary_key=True, default=generate_unique_key)
    project_id = Column(String(22))
    stage_id = Column(String, ForeignKey(Stage.stage_id, ondelete="CASCADE"))  
    reporter_id = Column(String)
    assignee_id = Column(String, default=None, nullable=True)
    sprint_id = Column(String, ForeignKey(Sprint.sprint_id, ondelete="CASCADE"))
    parent_id = Column(String, ForeignKey(task_id, ondelete="CASCADE"))
    task_name = Column(String)
    description = Column(Text)
    type = Column(String)
    status = Column(String, default=TaskStatus.TODO)
    priority = Column(String, default=Priorities.LOW)
    start_date = Column(DateTime(timezone=True), default=get_current_time)
    actual_start_date = Column(
        DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True), default=get_current_time)
    actual_end_date = Column(DateTime(timezone=True))

    def change_priority(self, status: Priorities):
        self.priority = status

    def change_status(self, status: TaskStatus):
        self.status = status

    def get_details(self):
        return {
            "task_id": self.task_id,
            "project_id": self.project_id,
            "stage_id": self.stage_id,
            "reporter_id": self.reporter_id,
            "assignee_id": self.assignee_id,
            "sprint_id": self.sprint_id,
            "parent_id": self.parent_id,
            "task_name": self.task_name,
            "description": self.description,
            "type": self.type,
            "status": self.status,
            "priority": self.priority,
            "start_date": self.start_date,
            "actual_start_date": self.actual_start_date,
            "end_date": self.end_date,
            "actual_end_date": self.actual_end_date,
        }
