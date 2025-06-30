from src.database import db
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from src.models import Employee

# LeavePolicy: global default rules
class LeavePolicy(db.Model):
    __tablename__ = "leave_policy"

    id = Column(Integer, primary_key=True)
    leave_type = Column(String, nullable=False)  
    default_days = Column(Float, nullable=False)