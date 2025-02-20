from src.database import db
from src.utils import get_current_time, generate_unique_key
from sqlalchemy import Column, String,  DateTime, ForeignKey
from .project import Project


class UsersRole:
    ADMIN ='ADMIN'
    PROJECT_LEAD = 'PROJECT_LEAD'
    REPORTER = 'REPORTER'
    ASSIGNEE = 'ASSIGNEE'

class UserAccess:
    GRANT = 'GRANT'
    REJECT = 'REJECT'
    INVITED ='INVITED'
    
class ProjectUsers(db.Model):
    __tablename__="project_users"

    associate_id = Column(String(22), primary_key=True, default=generate_unique_key)
    project_id = Column(String,  ForeignKey(Project.project_id, ondelete="CASCADE")) 
    employee_id = Column(String)
    role = Column(String)
    last_active = Column(DateTime(timezone=True))
    access_status = Column(String)
    associated_date = Column(DateTime(timezone=True), default=get_current_time)

    def get(self):
        return{
            "associate_id":self.associate_id,
            "project_id": self.project_id,
            "employee_id": self.employee_id ,
            "role": self.role,
            "last_active": self.last_active,
            "access_status": self.access_status,
            "associated_date": self.associated_date,
        }