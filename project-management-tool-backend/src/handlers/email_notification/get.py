from src.models import EmailNotification,Employee
from src.database import db
from sqlalchemy import select
from flask import jsonify


class EmailNotificationHandler:
    
    def __init__(self, request) -> None:
        self.request = request
        self.session = db.session()

    def get_all_notifications(self):
        try:
            stmt = select(EmailNotification)
            result = self.session.execute(stmt).scalars().all() 

            response = [{
                "notification_id": n.notification_id,
                "employee_id": n.employee_id,
                "employee_name": n.employee.name if n.employee else None, 
                "task_name": n.task_name,
                "stage_name": n.stage_name,
                "email": n.email,
                "project_name": n.project_name,
                "link": n.link,
                "created_time": n.created_time,
            } for n in result]

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
