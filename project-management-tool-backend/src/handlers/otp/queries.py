from sqlalchemy import select, update, delete
from src.models import Otp
from src.database import db

class OtpQueries:
    
    def __init__(self):
        self.session = db.session()

    def _check_otp(self):
        if self.otp_type=='mail':
            query = select(Otp).where(Otp.email==self.lookup)
        else:
            query = select(Otp).where(Otp.phone_number==self.lookup)

        result = self.session.execute(query).scalars().first()
        return result

    
    def _update_exp_time(self, otp_id, **kwargs):
        query = update(Otp).where(Otp.id==otp_id).values(**kwargs)
        self.session.execute(query)
        self.session.commit()

    
    def _delete_otp(self, otp_id):
        query = delete(Otp).where(Otp.id==otp_id)
        self.session.execute(query)
        self.session.commit()
    
    def _create_new_otp(self, otp_obj):
        self.session.add(otp_obj)
        self.session.commit()