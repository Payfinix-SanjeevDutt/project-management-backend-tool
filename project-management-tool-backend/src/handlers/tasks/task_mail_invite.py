from flask import jsonify
from src.events import Events
from src.handlers.tasks.createtask import *
from src.events import NotificationServiceManager
from src.models.project import Project  

class SendInvite:
    def __init__(self, request):
        self.request = request

    def get_project_name(self, project_id):
        """Fetch the project name from the Project model using project_id."""
        project = Project.query.filter_by(project_id=project_id).first()
        return project.name if project else None

    def send_assignee_notification(self):
        try:
            data = self.request.json

            username = data.get("username")
            task_name = data.get("task_name")
            stage = data.get("stage")
            email = data.get("email")
            project_id = data.get("project_id")
            link = data.get("link")
            all_emails = data.get("all_emails", [])
            
            if not all([username, task_name, stage, email, project_id]):
                return jsonify({"status": False, "message": "Missing required fields in the request"}), 400

            project_name = self.get_project_name(project_id)
            if not project_name:
                return jsonify({"status": False, "message": "Invalid project ID"}), 400

            mail_event_assignee = Events.ASSIGNEE_ASSIGNED(
                user_name=username,
                project_name=project_name,
                email=[email],
                stage=stage,
                task_name=task_name,
                link=link
            )

            nsmo = NotificationServiceManager()
            nsmo.send(mail_event_assignee)
            
            other_emails = [e for e in all_emails if e and e != email]
            if other_emails:
                mail_event_others = Events.OTHERS_NOTIFIED(
                    user_name=username,
                    project_name=project_name,
                    email=other_emails,
                    stage=stage,
                    task_name=task_name,
                    link=link
                )
                nsmo.send(mail_event_others)

            return jsonify({
                "status": True,
                "message": "Task Assignment notification sent to assignee successfully",
            }), 200

        except Exception as e:
            return jsonify({"status": False, "message": str(e)}), 500

    def send_reporter_notification(self):
        try:
            data = self.request.json
            username = data.get("username")
            task_name = data.get("task_name")
            stage = data.get("stage")
            email = data.get("email")
            project_id = data.get("project_id")
            link = data.get("link")



            if not all([username, task_name, stage, email, project_id]):
                return jsonify({"status": False, "message": "Missing required fields in the request"}), 400

            project_name = self.get_project_name(project_id)
            if not project_name:
                return jsonify({"status": False, "message": "Invalid project ID"}), 400

            mail_event_reporter = Events.REPORTER_ASSIGNED(
                user_name=username,
                project_name=project_name,
                email=[email],
                stage=stage,
                task_name=task_name,
                link = link
            )

            nsmo = NotificationServiceManager()
            nsmo.send(mail_event_reporter)

            return jsonify({
                "status": True,
                "message": "Task Assignment notification sent to reporter successfully",
            }), 200

        except Exception as e:
            return jsonify({"status": False, "message": str(e)}), 500
