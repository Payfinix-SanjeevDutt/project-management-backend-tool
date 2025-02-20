from sqlalchemy import select,update,delete
from flask import jsonify

from src.models import Employee
from src.database import db
from src.utils import generate_token


class LoginEmployee:
    def __init__(self, request) -> None:
        self.request = request
        self.session = db.session()

    def login(self):
        try:
            body = self.request.json
            email = body.get('email')
            password = body.get('password')

            employee = self.session.query(Employee).filter_by(email=email, password=password).first()
            if employee:
                return jsonify({
                    "status": True,
                    "error_code": 0,
                    "message": "User login successfully",
                    "data":{
                        "accessToken": generate_token(employee_id = employee.employee_id)  
                    }
                }), 200
            else:
                return jsonify({
                    "status": False,
                    "error_code": 1,
                    "message": "Invalid email or password",
                    "data":{
                        "accessToken":""
                    }
                }), 401

        except Exception as e:
            print(e)
            return jsonify({
                "status":False,
                "error_code":2,
                "message":f'error in login',
                "data":{
                    "accessToken":""   
                }
            }), 500    

    
            