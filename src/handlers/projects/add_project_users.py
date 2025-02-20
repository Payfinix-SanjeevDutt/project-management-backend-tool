import logging
from flask import request
from src.database import db
from src.models import ProjectUsers, Employee, Project


class CreateEmployeeUser:
    def __init__(self, request):
        self.request = request
        self.session = db.session()

    def create(self):
        try:
            body = self.request.json

            project_id = body.get('project_id')
            role = body.get('role', 'Member')
            employees = body.get('employees')

            if not project_id or not employees:
                return {
                    "status": False,
                    "error_code": 2,
                    "message": "Project ID or employee data is missing.",
                    "data": {}
                }

            new_assignment = []
            for employee in employees:
                new_assignment.append(ProjectUsers(
                    project_id=project_id,
                    employee_id=employee,
                    role=role
                ))

            self.session.add_all(new_assignment)
            self.session.commit()

            return {
                "status": True,
                "error_code": 0,
                "message": "Employees successfully added to project.",
                "data": body
            }
        except Exception as e:
            self.session.rollback()

            return {
                "status": False,
                "error_code": 6,
                "message": f"Error in creating user: {str(e)}",
                "data": {}
            }
