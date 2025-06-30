from src.database import db
from src.models import Holiday

class HolidayGetHandler:

    def __init__(self):
        self.session = db.session()

    def get(self, request):
        try:
            body = request.get_json()
            holiday_id = body.get('holiday_id')

            if not holiday_id:
                return {
                    "status": False,
                    "error": 1,
                    "message": "holiday_id is required in the request body",
                    "data": {}
                }

            holiday = self.session.query(Holiday).filter_by(holiday_id=holiday_id).first()

            if not holiday:
                return {
                    "status": False,
                    "error": 1,
                    "message": "Holiday not found",
                    "data": {}
                }

            return {
                "status": True,
                "error": 0,
                "message": "Holiday fetched successfully",
                "data": {
                    "holiday_id": holiday.holiday_id,
                    "holiday_name": holiday.holiday_name,
                    "start_date": holiday.start_date.isoformat(),
                    "end_date": holiday.end_date.isoformat(),
                    "is_optional": holiday.is_optional,
                    "type": holiday.type
                }
            }

        except Exception as e:
            return {
                "status": False,
                "error": 1,
                "message": f"Failed to fetch holiday due to {e}",
                "data": {}
            }
