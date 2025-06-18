from src.models import EmailNotification, Employee
from src.database import db
from sqlalchemy import select
from flask import jsonify


class GetEmailNotification:

    def __init__(self, request) -> None:
        self.request = request
        self.session = db.session()

    def get_notifications_by_employee_id(self):
        try:
            data = self.request.get_json()
            employee_id = data.get("employee_id")

            if not employee_id:
                return jsonify({
                    "status": False,
                    "error": 1,
                    "data": [],
                    "message": "Missing required field: employee_id"
                }), 400

            # Fetch notifications and join with Employee table
            stmt = select(EmailNotification).where(EmailNotification.employee_id == employee_id)
            result = self.session.execute(stmt).scalars().all()

            response = []
            for n in result:
                employee = n.employee
                response.append({
                    "notification_id": n.notification_id,
                    "employee_id": n.employee_id,
                    "employee_name": employee.name if employee else None,
                    "employee_avatar": employee.avatar if employee else None,  # 👈 Add avatar here
                    "task_name": n.task_name,
                    "stage_name": n.stage_name,
                    "email": n.email,
                    "project_name": n.project_name,
                    "link": n.link,
                    "created_time": n.created_time,
                })

            return jsonify({
                "status": True,
                "error": 0,
                "data": response,
                "message": "Email notifications retrieved successfully"
            }), 200

        except Exception as e:
            return jsonify({
                "status": False,
                "error": 5,
                "data": [],
                "message": f"Failed to retrieve email notifications: {str(e)}"
            }), 500

