from src.database import db
from src.models import Holiday

class HolidayUpdateHandler:

    def __init__(self):
        self.session = db.session()

    def update(self, request):
        try:
            body = request.get_json()
            holiday_id = body.get('holiday_id')

            if not holiday_id:
                return {
                    "status": False,
                    "error": 1,
                    "message": "holiday_id is required",
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

            # Update fields if present in request
            holiday.holiday_name = body.get('holiday_name', holiday.holiday_name)
            holiday.start_date = body.get('start_date', holiday.start_date)
            holiday.end_date = body.get('end_date', holiday.end_date)
            holiday.is_optional = body.get('is_optional', holiday.is_optional)
            holiday.type = body.get('type', holiday.type)

            self.session.commit()

            return {
                "status": True,
                "error": 0,
                "message": "Holiday updated successfully",
                "data": {
                    "holiday_id": holiday.holiday_id
                }
            }

        except Exception as e:
            self.session.rollback()
            return {
                "status": False,
                "error": 1,
                "message": f"Holiday update failed due to {e}",
                "data": {}
            }
