from src.models import EmailNotification,Employee
from src.database import db
from sqlalchemy import select
from flask import jsonify


class EmailNotificationHandler:
    def __init__(self, request) -> None:
        self.request = request
        self.body = request.get_json()
        self.session = db.session()

    def create_notification(self):
        try:
            required_fields = ['employee_id', 'task_name', 'email', 'project_name']

            missing = [field for field in required_fields if field not in self.body]
            if missing:
                return jsonify({
                    "status": False,
                    "error": 1,
                    "message": f"Missing required fields: {', '.join(missing)}"
                }), 400

            employee_id = self.body['employee_id']
            task_name = self.body['task_name']
            stage_name = self.body.get('stage_name') 
            email = self.body['email']
            project_name = self.body['project_name']
            link = self.body.get('link')

            new_notification = EmailNotification(
                employee_id=employee_id,
                task_name=task_name,
                stage_name=stage_name,
                email=email,
                project_name=project_name,
                link=link
            )

            self.session.add(new_notification)
            self.session.commit()

            return jsonify({
                "status": True,
                "error": 0,
                "message": "Email notification created successfully",
                "data": new_notification.get()
            }), 201

        except Exception as e:
            self.session.rollback()
            return jsonify({
                "status": False,
                "error": 5,
                "message": f"Failed to create email notification: {str(e)}"
            }), 500
