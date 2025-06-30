from src.database import db
from src.models import TimeLog
from datetime import datetime

class GetTimeLogWeekly:

    def __init__(self):
        self.session = db.session()

    def fetchweekly(self, request):
        try:
            body = request.json
            employee_id = body.get("employee_id")
            start_date_str = body.get("start_date")
            end_date_str = body.get("end_date")

            if not employee_id:
                return {
                    "status": False,
                    "error": 1,
                    "message": "Missing employee_id in request",
                    "data": []
                }

            if not start_date_str or not end_date_str:
                return {
                    "status": False,
                    "error": 1,
                    "message": "Missing start_date or end_date in request",
                    "data": []
                }

            # Parse dates
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            except ValueError:
                return {
                    "status": False,
                    "error": 1,
                    "message": "Invalid date format. Use YYYY-MM-DD.",
                    "data": []
                }

            # Build query
            query = self.session.query(TimeLog).filter(
                TimeLog.employee_id == employee_id,
                TimeLog.date >= start_date,
                TimeLog.date <= end_date
            )

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
