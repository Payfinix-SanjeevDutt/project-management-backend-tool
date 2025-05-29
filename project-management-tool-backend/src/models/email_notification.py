from src.database import db
from src.utils import get_current_time, generate_unique_key
from sqlalchemy import Column, String, DateTime, ForeignKey
from src.models.employee import Employee  
from sqlalchemy.orm import relationship
 
 
class EmailNotification(db.Model):
    
    __tablename__ = "email_notifications"
 
    notification_id = Column(String(22), primary_key=True, default=generate_unique_key)
    employee_id = Column(String(22), ForeignKey(Employee.employee_id, ondelete="CASCADE"), nullable=False)
    task_name = Column(String, nullable=False)
    stage_name = Column(String, nullable=True)
    project_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    link = Column(String, nullable=True)
    created_time = Column(DateTime(timezone=True), default=get_current_time)
 
    employee = relationship("Employee", backref="notifications")
 
 
    def get(self):
        return {
            "notification_id": self.notification_id,
            "employee_id": self.employee_id,
            "task_name": self.task_name,
            "stage_name": self.stage_name,
            "email": self.email,
            "project_name": self.project_name,
            "link": self.link,
            "created_time": self.created_time,
        }
 
 