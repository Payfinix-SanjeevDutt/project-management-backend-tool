from src.database import db
from src.utils import get_current_time, generate_unique_key
from sqlalchemy import Column, String, Text, DateTime


class ProjectStatus:
    ON_GOING = 'ON_GOING'
    MAINTENANCE ='MAINTENANCE'   
    COMPLETED = 'COMPLETED'
    PLANNED = 'PLANNED'
    CANCELLED = 'CANCELLED'
    ONHOLD = 'ON_HOLD' 

class Project(db.Model):
    __tablename__="projects"

    project_id = Column(String(22), primary_key=True, default=generate_unique_key)
    name = Column(String)
    status = Column(String)
    description = Column(Text)
    start_date = Column(DateTime(timezone=True), default=get_current_time)
    end_date = Column(DateTime(timezone=True), default=get_current_time)
    actual_start_date = Column(DateTime(timezone=True), nullable=True)
    actual_end_date = Column(DateTime(timezone=True), nullable=True)
    cover_img = Column(String)

    def get(self):
        return {
            "project_id": self.project_id,
            "name": self.name,
            "status": self.status,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "actual_start_date": self.actual_start_date,
            "actual_end_date": self.actual_end_date,
            "cover_img": self.cover_img
        }
