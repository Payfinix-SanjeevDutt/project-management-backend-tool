from src.database import db
from src.utils import generate_unique_key
from sqlalchemy import Column, String, Date
from sqlalchemy.sql import func

class IsOptional:
    true = "True"
    false = "False"
    
class Type:
    public_holiday = "Public"
    religious_holiday = "Religious"
    national_holiday = "National"
    other = "Other"


class Holiday(db.Model):
    
    __tablename__ = "holiday"
    
    holiday_id = Column(String(22), primary_key = True, default=generate_unique_key)
    holiday_name = Column(String, nullable=False)
    start_date = Column(Date, default=func.current_date(), nullable=False)
    end_date = Column(Date,nullable=False)
    is_optional = Column(String, default=IsOptional.false)
    type = Column(String, default=Type.public_holiday)
    