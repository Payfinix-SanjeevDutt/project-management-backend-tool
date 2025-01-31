from sqlalchemy import String , Column , ForeignKey ,DateTime
from src.utils import generate_unique_key,get_current_time
from src.database import db
from src.models import Employee,Task
from sqlalchemy.orm import relationship

class Comments(db.Model):

    __tablename__ = "comments"

    comment_id = Column(String(22),primary_key=True , default= generate_unique_key)
    employee_id = Column(String,ForeignKey(Employee.employee_id))
    task_id = Column(String(22), ForeignKey(Task.task_id,ondelete= "CASCADE"))
    date= Column(DateTime(timezone=True), default=get_current_time)
    action=Column(String)
    value=Column(String)

    employee = relationship("Employee", backref="comments")
