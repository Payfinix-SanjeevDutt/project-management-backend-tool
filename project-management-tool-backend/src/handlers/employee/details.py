from src.models import Employee
from src.database import db
from sqlalchemy import select, update, delete
from flask import jsonify


class EmployeeHandler:
    def __init__(self, request) -> None:
        self.request = request
        self.body = None
        self.session = db.session()

    def getemployees(self):
        try:
            stmt = select(Employee)
            result = self.session.execute(stmt).all()

            response = [{
                "employee_id": emp.employee_id,
                "employee_name": emp.name,
                "employee_email": emp.email,
                "mobile": emp.mobile,
                "verification": emp.verification,
                "employee_avatar": emp.avatar,
                "role": emp.job_title,
                "access_status": None,
                # "role": None,
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
