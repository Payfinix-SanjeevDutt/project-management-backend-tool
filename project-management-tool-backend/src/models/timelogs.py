from sqlalchemy import String, Column, Date, Time, ForeignKey, Boolean
from src.database import db
from src.models import Employee
from src.utils import generate_unique_key
from sqlalchemy.sql import func


class TimeLog(db.Model):
    __tablename__ = "timelog"

    log_id = Column(String, primary_key=True, default=generate_unique_key)
    employee_id = Column(String, ForeignKey(Employee.employee_id), nullable=False)

    date = Column(Date, default=func.current_date(), nullable=False)
    clock_in = Column(Time, nullable=True)
    clock_out = Column(Time, nullable=True)
    total_hours = Column(Time, nullable=True)

    def __repr__(self):
        return f"<TimeLog {self.employee_id} | {self.date} | {self.clock_in} - {self.clock_out}>"
