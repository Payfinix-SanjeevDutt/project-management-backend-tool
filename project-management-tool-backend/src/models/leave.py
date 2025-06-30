from src.database import db
from src.utils import generate_unique_key
from sqlalchemy import Column, String, Date, Boolean, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.models import Employee

class LeaveType:
    sick = "Sick"
    casual = "Casual"
    unpaid = "Unpaid"
    comp_off = "Comp-Off"
    maternity = "Maternity"
    paternity = "Paternity"



class Leave(db.Model):
    
    __tablename__ = "leave"

    leave_id = Column(String(22), primary_key=True, default=generate_unique_key)
    employee_id = Column(String, ForeignKey(Employee.employee_id), nullable=False)
    leave_type = Column(String, nullable=False, default=LeaveType.casual)
    start_date = Column(Date, default=func.current_date(), nullable=False)
    end_date = Column(Date, nullable=False)
    is_half_day = Column(Boolean, default=False)
    reason = Column(String(225), nullable=True)
    applied_on = Column(Date, default=func.current_date(), nullable=False)
    
    employee = relationship("Employee", backref="leaves")
  