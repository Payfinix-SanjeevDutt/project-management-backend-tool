from src.models import Employee,Task
from src.database import db
from sqlalchemy import select
from flask import jsonify


class EmployeeTaskHandler:
    def __init__(self, request) -> None:
        self.request = request
        self.body = None
        self.session = db.session()

    def employeeTaskList(self):
        try:
            stmt = select(Employee)
            result = self.session.execute(stmt).all()

            response = [{
                "employee_id": emp.employee_id,
                "employee_name": emp.name,
                "employee_email": emp.email,
                "verification": emp.verification,
                "employee_avatar": emp.avatar,
                "access_status": None,
                "role": None,
            } for emp, in result]

            return jsonify({
                "status": True,
                "error": 0,
                "data": response,
                "message": " employees details are displayed successfully"
            }), 200

        except Exception as e:
            return jsonify({
                "status": False,
                "error": 5,
                "data": [],
                "message": f'employees dislpay failed as {e}'
            }), 500
