from src.models import EmailNotification
from src.database import db
from sqlalchemy import delete
from flask import jsonify

class DeleteEmailNotification:
    def __init__(self, request) -> None:
        self.request = request
        self.body = None
        self.session = db.session()

    def delete(self):
        self.body = self.request.json
        if not self.validate_request():
            return jsonify({
                "message": "notification_id not found in request body",
                "error_code": 6
            }), 404

        try:
            statement = delete(EmailNotification).where(EmailNotification.notification_id == self.body['notification_id'])
            result = self.session.execute(statement)
            self.session.commit()

            if result.rowcount == 0:
                return jsonify({
                    "message": "No notification found with the given ID",
                    "error_code": 1
                }), 404

            return jsonify({
                "message": "Notification deleted successfully",
                "error_code": 0
            }), 200

        except Exception as e:
            self.session.rollback()
            return jsonify({
                "message": f"Failed to delete notification: {str(e)}",
                "error_code": 2
            }), 500

    def validate_request(self):
        return "notification_id" in self.body
