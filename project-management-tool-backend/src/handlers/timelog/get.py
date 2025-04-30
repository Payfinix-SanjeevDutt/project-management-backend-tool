from src.database import db
from src.models import TimeLog


class GetTimeLog:

    def __init__(self):
        self.session = db.session()

    def fetch(self, request):
        try:
            body = request.json
            employee_id = body.get("employee_id")

            query = self.session.query(TimeLog)
            if not employee_id:
                return {
                    "status": False,
                    "error": 1,
                    "message": "Missing employee_id in request",
                    "data": []
                }


            if employee_id:
                query = query.filter(TimeLog.employee_id == employee_id)

            logs = query.order_by(TimeLog.date.desc()).all()

            data = [
                {
                    "log_id": log.log_id,
                    "employee_id": log.employee_id,
                    "date": str(log.date),
                    "clock_in": log.clock_in.strftime('%H:%M') if log.clock_in else None,
                    "clock_out": log.clock_out.strftime('%H:%M') if log.clock_out else None,
                    "total_hours": log.total_hours.strftime('%H:%M') if log.total_hours else None,
                }
                for log in logs
            ]

            return {
                "status": True,
                "error": 0,
                "message": "Time logs fetched successfully",
                "data": data
            }

        except Exception as e:
            return {
                "status": False,
                "error": 1,
                "message": f"Failed to fetch time logs: {e}",
                "data": []
            }
