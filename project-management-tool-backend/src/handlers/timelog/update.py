from src.database import db
from src.models import TimeLog


class UpdateTimeLog:

    def __init__(self):
        self.session = db.session()

    def update(self, request):
        try:
            body = request.json
            timelog_id = body.get("log_id")

            if not timelog_id:
                return {
                    "status": False,
                    "error": 1,
                    "message": "Missing timelog_id in request",
                    "data": []
                }

            timelog = self.session.query(TimeLog).filter_by(log_id=timelog_id).first()

            if not timelog:
                return {
                    "status": False,
                    "error": 1,
                    "message": f"No TimeLog found with id: {timelog_id}",
                    "data": []
                }

            if "clock_in" in body:
                timelog.clock_in = body["clock_in"]
            if "clock_out" in body:
                timelog.clock_out = body["clock_out"]
            if "total_hours" in body:
                timelog.total_hours = body["total_hours"]

            self.session.commit()

            return {
                "status": True,
                "error": 0,
                "message": "TimeLog updated successfully",
                "data": {
                    "log_id": timelog.log_id,
                    "employee_id": timelog.employee_id,
                    "date": str(timelog.date)
                }
            }

        except Exception as e:
            self.session.rollback()
            return {
                "status": False,
                "error": 1,
                "message": f"Failed to update TimeLog: {e}",
                "data": []
            }
