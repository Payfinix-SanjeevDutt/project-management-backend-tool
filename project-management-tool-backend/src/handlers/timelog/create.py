from src.database import db
from src.models import TimeLog


class CreateTimeLog:

    def __init__(self):
        self.session = db.session()

    def create(self, request):
        try:
            body = request.json

            timelog = TimeLog(
                employee_id=body['employee_id'],
                date=body['date'],
                clock_in=body.get('clock_in'),
                clock_out=body.get('clock_out'),
                total_hours=body.get('hours_worked'),
            )

            self.session.add(timelog)
            self.session.commit()

            return {
                "status": True,
                "error": 0,
                "message": "Time log created successfully",
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
                "message": f"Time log creation failed: {e}",
                "data": {}
            }
