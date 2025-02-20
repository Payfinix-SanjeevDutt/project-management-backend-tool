from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from src.database import db
from src.models import Task, Employee
from src.utils import get_current_time, generate_unique_key


class History(db.Model):
    __tablename__ = 'history'

    history_id = Column(String, primary_key=True, default=generate_unique_key)
    task_id = Column(String, ForeignKey(Task.task_id, ondelete="CASCADE"))
    timestamp = Column(DateTime(timezone=True), default=get_current_time)
    employee_id = Column(String, ForeignKey(
        Employee.employee_id), nullable=False)
    description = Column(String)
