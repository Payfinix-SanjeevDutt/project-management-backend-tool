from src.database import db
from src.models import Holiday


class HolidayListHandler:

    def __init__(self):
        self.session = db.session()

    def list(self):
        try:
            holidays = self.session.query(Holiday).all()

            holiday_data = [
                {
                    "holiday_id": h.holiday_id,
                    "holiday_name": h.holiday_name,
                    "start_date": h.start_date.isoformat(),
                    "end_date": h.end_date.isoformat(),
                    "is_optional": h.is_optional,
                    "type": h.type
                }
                for h in holidays
            ]

            return {
                "status": True,
                "error": 0,
                "message": "Holiday list fetched successfully",
                "data": holiday_data
            }
        
        except Exception as e:
            return {
                "status": False,
                "error": 1,
                "message": f"Failed to fetch holidays due to {e}",
                "data": []
            }
