from src.models import Employee
from src.database import db
from sqlalchemy import select,update,delete
from flask import jsonify
from ..otp.actions import OtpHandler


class PasswordReset:
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

    def reset(self):
        try:
            self.body = self.request.json
            email = self.body.get("email")
            otp = self.body.get("otp")
            password = self.body.get("password")

            if not email or not otp or not password:
                 return jsonify({
                        "status":True,
                        "error_code":1,
                        "message":"one of the field is missing",
                    }), 400

            employee = self._get_employee(email)
            if not employee:
                 return jsonify({
                        "status":True,
                        "error_code":2,
                        "message":"employee does not exists",
                    }), 401

            otp = self._handle_otp(email, otp)
            if otp.code!='VERIFIED':
                return jsonify({
                        "status":True,
                        "error_code":3,
                        "message":f"{otp.info}",
                    }), 401

            employee.password = password
            self.session.add(employee)
            self.session.commit()
            return jsonify({
                        "status":True,
                        "error_code":0,
                        "message":"password reset",
                    }), 200
        
        except Exception as e:
            return jsonify({
                "status":False,
                "error_code":5,
                "message":f'{e}',
            }), 500
