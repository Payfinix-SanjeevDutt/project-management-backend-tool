from src.database import db
from src.models import Leave
from flask import request
from datetime import datetime


class CreateLeave:
    def __init__(self):
        self.session = db.session()

    def create(self, request):
        try:
            body = request.json

            leave = Leave(
                employee_id=body["employee_id"],
                leave_type=body.get("leave_type", "Casual"),
                start_date=datetime.strptime(body["start_date"], "%Y-%m-%d").date(),
                end_date=datetime.strptime(body["end_date"], "%Y-%m-%d").date(),
                is_half_day=body.get("is_half_day", False),
                reason=body.get("reason")
            )

            self.session.add(leave)
            self.session.commit()

            return {
                "status": True,
                "error": 0,
                "message": "Leave created successfully",
                "data": {
                    "leave_id": leave.leave_id,
                    "employee_id": leave.employee_id,
                    "leave_type": leave.leave_type
                }
            }

        except Exception as e:
            self.session.rollback()
            return {
                "status": False,
                "error": 1,
                "message": f"Failed to create leave: {str(e)}",
                "data": {}
            }
