from src.models import Employee
from src.database import db
from sqlalchemy import select,update,delete
from flask import jsonify


class UpdateEmployee:
    def __init__(self, request) -> None:
        self.request = request
        self.body = None
        self.session = db.session()

    def validatePayload(self):
        if "employee_id" not in self.body:
           return False
        return True

    def update(self):
     try:
        self.body = self.request.json

        update_employee = update(Employee).where(Employee.employee_id == self.body['employee_id']).values(
            name =self.body.get('name'),
            mobile=self.body.get('mobile'),
            address=self.body.get('address'),
            avatar=self.body.get('avatar'),
            organization=self.body.get('organization'),
            department=self.body.get('department'),
            job_title=self.body.get('job_title'),
        )
        
        self.session.execute(update_employee)
        self.session.commit()
        
        return jsonify({
                    "status": True,
                    "error_code": 0,
                    "message": "Employee updated successfully",
                    "data": {}
                }), 200
        
     except Exception as e:
        return {
            "status": False,
            "error_code": 5,
            "message": f'Employee update failed due to: {e}'
        }
