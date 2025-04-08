from sqlalchemy import String, Column, Date, Text, ForeignKey, Time
from src.database import db
from src.models import Employee
from src.utils import generate_unique_key
from sqlalchemy.sql import func


class TaskTimesheet:
    BILLABLE = "BILLABLE"
    NON_BILLABLE = "NON_BILLABLE"


class Timesheet(db.Model):
    __tablename__ = "timesheet"

    timesheet_id = Column(String, primary_key=True, default=generate_unique_key)
    employee_id = Column(String, ForeignKey(Employee.employee_id), nullable=False)
    projectName = Column(String)
    jobName = Column(String)
    workItem = Column(String)
    description = Column(Text)
    totalHours = Column(Time)
    startDate = Column(Date, default=func.current_date(), nullable=False)  # No Unique
    billable_status = Column(String, default=TaskTimesheet.BILLABLE)
