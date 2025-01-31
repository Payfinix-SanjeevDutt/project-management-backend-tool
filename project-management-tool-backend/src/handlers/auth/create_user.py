from sqlalchemy import select,update,delete
from flask import jsonify
from src.models import Employee
from src.database import db
from ..otp.actions import OtpHandler


class CreateEmployee:
    def __init__(self, request) -> None:
        self.request = request
        self.session = db.session()

    def create(self):
        try:
            body = self.request.json
            
            query = select(Employee).where(Employee.email==body['email'])
            result = self.session.execute(query).first()
            
            if result:
                return jsonify({
                    "status":True,
                    "error_code":2,
                    "message":"user already exists",
                }), 404

            employee = Employee(
                name=body['name'],
                email=body['email'],
                password = body['password'],
            )
            
            self.session.add(employee)
            self.session.commit()
            
            hander = OtpHandler(body['email'])
            info = hander.send_otp()
            print(info.info, info.code)

            return jsonify({
                "status":True,
                "error_code":0,
                "message":"user added succesfully",
            }), 200
            
        except Exception as e:
            print(e)
            return jsonify({    
                "status":False,
                "error_code":5,
                "message":f'error in creating user',
            }), 500
            