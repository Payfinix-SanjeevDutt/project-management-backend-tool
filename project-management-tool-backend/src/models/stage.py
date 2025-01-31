from sqlalchemy import String, Column, DateTime, Text,ForeignKey
from src.utils import get_current_time, generate_unique_key
from src.database import db
from src.models.project import Project


class Stage(db.Model):

    __tablename__ = "stages"

    stage_id = Column(String(22), primary_key=True, default=generate_unique_key)
    project_id = Column(String(22),ForeignKey(Project.project_id, ondelete="CASCADE"))
    name = Column(String)
    description = Column(Text)
    start_date = Column(DateTime(timezone=True), default=get_current_time)
    end_date = Column(DateTime(timezone=True), default=get_current_time)
    actual_start_date = Column(DateTime(timezone=True),nullable=True)
    actual_end_date = Column(DateTime(timezone=True),nullable=True)
