from flask import jsonify
from sqlalchemy import select
from src.database import db
from src.models import Employee, Verification
from src.utils import generate_token
from ..otp.actions import OtpHandler

class UserVerify:
    def __init__(self, request) -> None:
        self.request = request
        self.session = db.session()
        
    def _get_employee(self, email:str) -> Employee | None:
        query = select(Employee).where(Employee.email==email)
        result:Employee | None = self.session.execute(query).scalars().first()
        return result

    def _handle_otp(self, email, otp):
        hander = OtpHandler(email)
        info = hander.verify_otp(otp)
        return info

    def verify(self):
        try:
            
            body = self.request.json
            
            employeeObj = self._get_employee(body['email'])

            if employeeObj == None:
                return jsonify({
                    "status":True,
                    "error_code":3,
                    "message":"user not exists",
                }), 404
                
            
            isVerified = self._handle_otp(body['email'], body['otp'])

            if isVerified.code=='VERIFIED':
                employeeObj.change_verification(Verification.VERIFIED)
                self.session.add(employeeObj)
                self.session.commit()
                
                return jsonify({
                    "status":True,
                    "error_code":0,
                    "message":f"{isVerified.info}",
                    "data":{
                        "accessToken":generate_token(employee_id = employeeObj.employee_id),        
                    }
                }), 200

            employeeObj.change_verification(Verification.REJECT)
            self.session.add(employeeObj)
            self.session.commit()
            
            return jsonify({
                    "status":True,
                    "error_code":1,
                    "message":f"{isVerified.info}",
                    "data":{
                        "accessToken":"" 
                    }
                }), 200
            
        except Exception as e:
            return jsonify({
                "status":False,
                "error_code":2,
                "message":f'{e}',
                "data":{
                    "accessToken":""   
                }
            }), 500
            