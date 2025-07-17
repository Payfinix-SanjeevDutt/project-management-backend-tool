from src.database import db
from src.models import TimeLog
from datetime import datetime, timedelta

class GetTimeLog:

    def __init__(self):
        self.session = db.session()

    def fetch(self, request):
        try:
            body = request.json
            employee_id = body.get("employee_id")

            if not employee_id:
                return {
                    "status": False,
                    "error": 1,
                    "message": "Missing employee_id in request",
                    "data": []
                }

            query = self.session.query(TimeLog).filter(TimeLog.employee_id == employee_id)
            logs = query.order_by(TimeLog.date.desc()).all()

            delay_count = 0
            data = []
            delay_details = []
            
            for log in logs:
                # Skip if no total_hours recorded
                if not log.total_hours:
                    data.append({
                        "log_id": log.log_id,
                        "employee_id": log.employee_id,
                        "date": str(log.date),
                        "clock_in": log.clock_in.strftime('%H:%M') if log.clock_in else None,
                        "clock_out": log.clock_out.strftime('%H:%M') if log.clock_out else None,
                        "total_hours": None,
                        "is_delay": False,
                        "missed_time": None
                    })
                    continue
                
                # Convert total_hours to timedelta
                try:
                    hours, minutes = map(int, log.total_hours.strftime('%H:%M').split(':'))
                    total_hours_td = timedelta(hours=hours, minutes=minutes)
                except Exception as e:
                    print(f"Error parsing time for log {log.log_id}: {e}")
                    continue
                
                # 8 hours as timedelta
                full_day = timedelta(hours=8)
                
                # Check if it's a delay day (less than 8 hours)
                is_delay = total_hours_td < full_day
                missed_time = str(full_day - total_hours_td) if is_delay else None
                
                if is_delay:
                    delay_details.append({
                        "date": str(log.date),
                        "total_hours": log.total_hours.strftime('%H:%M'),
                        "missed_time": missed_time
                    })
                    delay_count += 1
                data.append({
                    "log_id": log.log_id,
                    "employee_id": log.employee_id,
                    "date": str(log.date),
                    "clock_in": log.clock_in.strftime('%H:%M') if log.clock_in else None,
                    "clock_out": log.clock_out.strftime('%H:%M') if log.clock_out else None,
                    "total_hours": log.total_hours.strftime('%H:%M'),
                    "is_delay": is_delay,
                    "missed_time": missed_time
                })

            return {
                "status": True,
                "error": 0,
                "message": "Time logs fetched successfully",
                "data": data,
                "delay_count": delay_count,
                "delay_details": delay_details
            }

        except Exception as e:
            return {
                "status": False,
                "error": 1,
                "message": f"Failed to fetch time logs: {e}",
                "data": []
            }