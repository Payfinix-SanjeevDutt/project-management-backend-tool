from src.database import db
from src.utils import generate_unique_key, get_current_time
from sqlalchemy import Column, String, DateTime, Text



class Verification:
    
    VERIFIED = 'VERIFIED'
    PENDING = 'PENDING'
    REJECT = 'REJECT'
    

class Employee(db.Model):
    __tablename__="employees"

    employee_id = Column(String(22), primary_key=True, default=generate_unique_key)
    name = Column(String)
    email = Column(String)
    mobile = Column(String)
    job_title = Column(String)
    organization = Column(String)
    department = Column(String)
    address = Column(Text)
    password = Column(String)
    verification = Column(String, default=Verification.PENDING)
    avatar = Column(String)
    created_date = Column(DateTime(timezone=True), default=get_current_time)


    def change_verification(self, status:Verification):
        self.verification = status

    def get_details(self):
        return {
            "employee_id": self.employee_id,
            "name": self.name,
            "email": self.email,
            "mobile": self.mobile,
            "address":self.address,
            "job_title":self.job_title,
            "organization":self.organization,
            "department":self.department,
            "verification": self.verification,
            "avatar": self.avatar,
            "created_date": self.created_date
        }