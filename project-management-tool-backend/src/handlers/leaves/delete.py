# src/handlers/leave_delete_handler.py

from src.database import db
from src.models import Leave


class LeaveDeleteHandler:
    def __init__(self):
        self.session = db.session()

    def delete(self, request):
        try:
            body = request.json
            leave_id = body.get("leave_id")

            if not leave_id:
                return {
                    "status": False,
                    "error": 1,
                    "message": "Missing leave_id in request.",
                    "data": {}
                }

            leave = self.session.query(Leave).filter_by(leave_id=leave_id).first()

            if not leave:
                return {
                    "status": False,
                    "error": 1,
                    "message": "Leave not found.",
                    "data": {}
                }

            self.session.delete(leave)
            self.session.commit()

            return {
                "status": True,
                "error": 0,
                "message": "Leave deleted successfully.",
                "data": {
                    "leave_id": leave_id
                }
            }

        except Exception as e:
            self.session.rollback()
            return {
                "status": False,
                "error": 1,
                "message": f"Failed to delete leave: {str(e)}",
                "data": {}
            }
