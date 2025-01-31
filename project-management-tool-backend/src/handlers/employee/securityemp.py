from src.database import db
from src.models import Employee
from sqlalchemy import select
from flask import jsonify


class SecurityEmpoyee:
    def __init__(self, request):
        self.request = request
        self.db = db.session()

    def security(self):
        try:
            body = self.request.json

            emp_id = select(Employee).where(Employee.employee_id == body['employee_id'])
            result = self.db.execute(emp_id).scalars().first()
            print(result)

            if not result:
                return jsonify({
                "status": False,
                "error_code": 2,
                "message": "Employee not found"
            }), 404


            if result.password == body['old_password']:

                result.password = body['new_password']
                self.db.add(result)
                self.db.commit()

                return jsonify ({
                    "status":True,
                    "error_code":0,
                    "message":"password updated successfully",
                }), 200


            return jsonify({
                    "status": False,
                    "error_code": 1,
                    "message": "Old password is incorrect",
                }), 400
        
        except Exception as e:
            print(e)
            return jsonify({    
                "status":False,
                "error_code":5,
                "message":f'error in changing password',
            }), 500
    