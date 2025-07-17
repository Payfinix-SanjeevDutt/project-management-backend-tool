# from src.models import Employee
# from src.database import db
# from sqlalchemy import select, update, delete
# from flask import jsonify


# class EmployeeHandler:
#     def __init__(self, request) -> None:
#         self.request = request
#         self.body = None
#         self.session = db.session()

#     def getemployees(self):
#         try:
#             stmt = select(Employee)
#             result = self.session.execute(stmt).all()

#             response = [{
#                 "employee_id": emp.employee_id,
#                 "employee_name": emp.name,
#                 "employee_email": emp.email,
#                 "mobile": emp.mobile,
#                 "verification": emp.verification,
#                 "employee_avatar": emp.avatar,
#                 "role": emp.job_title,
#                 "access_status": None,
#                 # "role": None,
#             } for emp, in result]

#             return jsonify({
#                 "status": True,
#                 "error": 0,
#                 "data": response,
#                 "message": " employees details are displayed successfully"
#             }), 200

#         except Exception as e:
#             return jsonify({
#                 "status": False,
#                 "error": 5,
#                 "data": [],
#                 "message": f'employees dislpay failed as {e}'
#             }), 500



from src.models import Employee
from src.database import db
from sqlalchemy import select
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
            } for emp, in result]

            return jsonify({
                "status": True,
                "error": 0,
                "data": response,
                "message": "Employees details displayed successfully"
            }), 200

        except Exception as e:
            return jsonify({
                "status": False,
                "error": 5,
                "data": [],
                "message": f"Employees display failed: {e}"
            }), 500

    def get_employee_by_id(self, employee_id):
        try:
            stmt = select(Employee).where(Employee.employee_id == employee_id)
            result = self.session.execute(stmt).first()

            if not result:
                return jsonify({
                    "status": False,
                    "error": 2,
                    "data": [],
                    "message": "Employee not found"
                }), 404

            emp = result[0]

            response = {
                "employee_id": emp.employee_id,
                "employee_name": emp.name,
                "employee_email": emp.email,
                "mobile": emp.mobile,
                "verification": emp.verification,
                "employee_avatar": emp.avatar,
                "role": emp.job_title,
                "access_status": None,
            }

            return jsonify({
                "status": True,
                "error": 0,
                "data": response,
                "message": "Employee details fetched successfully"
            }), 200

        except Exception as e:
            return jsonify({
                "status": False,
                "error": 3,
                "data": [],
                "message": f"Failed to fetch employee: {e}"
            }), 500
