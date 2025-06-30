from src.database import db
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from src.models import Employee

class LeaveBalance(db.Model):
    __tablename__ = "leave_balance"

    id = Column(Integer, primary_key=True)
    employee_id = Column(String, ForeignKey(Employee.employee_id), nullable=False)
    leave_type = Column(String, nullable=False)
    balance = Column(Float, nullable=False)