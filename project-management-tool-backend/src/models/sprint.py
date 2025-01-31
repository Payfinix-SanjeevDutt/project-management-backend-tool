from sqlalchemy import String, Column, DateTime, Text
from src.utils import get_current_time, generate_unique_key
from src.database import db


class Sprint(db.Model):

    __tablename__ = "sprints"

    sprint_id = Column(String(22), primary_key=True, default=generate_unique_key)
    project_id = Column(String)
    name = Column(String)
    description = Column(Text)
    created_by = Column(String)
    created_at = Column(DateTime(timezone=True), default=get_current_time)
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    actual_start_date = Column(DateTime(timezone=True))
    actual_end_date = Column(DateTime(timezone=True))
