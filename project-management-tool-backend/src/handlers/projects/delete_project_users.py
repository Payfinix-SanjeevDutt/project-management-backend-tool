from flask import request
from sqlalchemy import delete
from src.database import db
from src.models import ProjectUsers

class DeleteProjectUsers:
    def __init__(self, request):
        self.request = request
        self.session = db.session()

    def delete(self):
        try:
            data = self.request.json
            project_id = data.get('project_id')
            employee_id = data.get('employee_id')

            if not project_id or not employee_id:
                return {
                    "status": False,
                    "error_code": 2,
                    "message": "Both project_id and employee_id are required.",
                    "data": {}
                }

            delete_query = (
                delete(ProjectUsers)
                .where(ProjectUsers.project_id == project_id)
                .where(ProjectUsers.employee_id == employee_id)
            )

            result = self.session.execute(delete_query)
            self.session.commit()

            if result.rowcount == 0:
                return {
                    "status": False,
                    "error_code": 3,
                    "message": "No user found with the given project_id and employee_id.",
                    "data": {}
                }

            return {
                "status": True,
                "error_code": 0,
                "message": "User removed from the project successfully.",
                "data": {}
            }

        except Exception as e:
            self.session.rollback()
            return {
                "status": False,
                "error_code": 1,
                "message": f"Failed to delete project user due to: {e}",
                "data": {}
            }
