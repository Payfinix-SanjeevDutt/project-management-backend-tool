from flask import jsonify
from src.models import Employee
from src.database import db
from src.utils import decode_token

class AccessTokenHandler:
    def __init__(self, request) -> None:
        self.request = request
        self.token  = self.request.headers['authorization'].split(' ')[1]
        self.body = None
        self.session = db.session()

    def getAccessToken(self):
        try:
            decoded_data = decode_token(self.token)
            employee_id = decoded_data.get('employee_id', '')

            employee = self.session.query(Employee).filter_by(employee_id=employee_id).first()
         
            if employee:
                return jsonify({
                    "status": False,
                    "error_code": 0,
                    "message": "Employee not verified.",
                    "data": employee.get_details()
                }), 200

            return jsonify({
                "status": False,
                "error_code": 1,
                "message": "Employee ID not found in the token.",
                "data": {}
            }), 401
                
               
        except Exception as e:
            return jsonify({
                "status":False,
                "error":5,
                "data":{},
                "message":f'access tokek failed : {e}'
            }), 500
            