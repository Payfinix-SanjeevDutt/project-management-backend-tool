from flask import request
from sqlalchemy import select, join
from sqlalchemy.orm import aliased
from src.database import db
from src.models import ProjectUsers, Employee

class ListProjectUsers:
    def __init__(self, request):
        self.request = request
        self.session = db.session()

    def list(self):
        try:
            project_id = self.request.json.get('project_id')

            if not project_id:
                return {
                    "status": False,
                    "error_code": 2,
                    "message": "Project ID is missing from the request.",
                    "data": {}
                }

            employee_alias = aliased(Employee, name="employee")

            query = (
                select(
                    ProjectUsers,
                    employee_alias.name.label("employee_name"),
                    employee_alias.email.label("employee_email"),
                    employee_alias.mobile.label("mobile"),
                    employee_alias.job_title.label("employee_job_title"),
                    employee_alias.organization.label("employee_organization"),
                    employee_alias.department.label("employee_department"),
                    employee_alias.avatar.label("employee_avatar"),
                )
                .select_from(ProjectUsers)
                .join(employee_alias, ProjectUsers.employee_id == employee_alias.employee_id)
                .where(ProjectUsers.project_id == project_id)  
            )

            result = self.session.execute(query).all()

            users = [
                {
                    **user[0].get(),
                    "employee_name": user.employee_name,
                    "employee_email": user.employee_email,
                    "mobile": user.mobile,
                    "employee_job_title": user.employee_job_title,
                    "employee_organization": user.employee_organization,
                    "employee_department": user.employee_department,
                    "employee_avatar": user.employee_avatar,
                }
                for user in result
            ]

            return {
                "status": True,
                "error_code": 0,
                "message": "Project users retrieved successfully",
                "data": users,
            }
        except Exception as e:
            return {
                "status": False,
                "error_code": 1,
                "message": f"Failed to retrieve project users due to {e}",
                "data": {},
            }
