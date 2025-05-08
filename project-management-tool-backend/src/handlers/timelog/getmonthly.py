from src.database import db
from src.models import TimeLog
from datetime import datetime

class GetEmpDetailsByMonth:

    def __init__(self):
        self.session = db.session()

    def emp_details_month(self, request):
        try:
            body = request.json
            employee_id = body.get("employee_id")
            start_date_str = body.get("start_date")  # Expected format: 'YYYY-MM-DD'
            end_date_str = body.get("end_date")

            
            if not employee_id or not start_date_str or not end_date_str:
                return {
                    "status": False,
                    "error": 1,
                    "message": "Employee ID, start date, and end date are required.",
                    "data": {}
                }

            
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

            
            logs = (
                self.session.query(TimeLog)
                .filter(TimeLog.employee_id == employee_id)
                .filter(TimeLog.date.between(start_date, end_date))
                .order_by(TimeLog.date.desc())
                .all()
            )

            
            log_list = [
                {
                    "date": str(log.date),
                    "clock_in": log.clock_in.strftime('%H:%M') if log.clock_in else None,
                    "clock_out": log.clock_out.strftime('%H:%M') if log.clock_out else None,
                    "total_hours": log.total_hours.strftime('%H:%M:%S') if log.total_hours else None
                }
                for log in logs
            ]

            return {
                "status": True,
                "error": 0,
                "message": "Time logs fetched successfully for given date range.",
                "data": {
                    "employee_id": employee_id,
                    "logs": log_list
                }
            }

        except Exception as e:
            return {
                "status": False,
                "error": 1,
                "message": f"Failed to fetch time logs: {e}",
                "data": {}
            }
