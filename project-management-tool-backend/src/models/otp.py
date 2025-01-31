from src.database import db
from src.utils import get_current_time, generate_unique_key, set_exp_time
from sqlalchemy import Column, String, Integer, DateTime


class Otp(db.Model):
    __tablename__ = 'otp'
    
    id = Column(String(22), default=generate_unique_key, primary_key=True )
    email = Column(String, unique=True)
    phone_number = Column(String, unique=True)
    otp = Column(String, nullable=False)
    created_time = Column(DateTime(timezone=True), default=get_current_time, nullable=False)
    expiration_time = Column(DateTime(timezone=True), default=set_exp_time, nullable=False)
    updated_time = Column(DateTime(timezone=True), default=get_current_time, nullable=True)
    resend_attempts = Column(Integer, default = 1, nullable=False)