from src.models import Employee
from src.database import db
from sqlalchemy import delete
from flask import jsonify

class DeleteEmployee:
        def __init__(self, request) -> None:
             self.request = request
             self.body = None
             self.session = db.session()

        def delete(self):
            self.body = self.request.json
            isValidate = self.validateProject()
            if not isValidate:
                response = {
                    "message":"id not found",
                    "error_code":6
                }
                return jsonify(response), 404

            statement = delete(Employee).where(Employee.employee_id == self.body['employee_id'])
            print(statement)
            self.session.execute(statement)
            self.session.commit()

            return jsonify({
                "message":"project deleted",
                "error_code":0
            }), 200
        
        def validateProject(self):
            if "emp_id" not in self.body:
               return False
            return True