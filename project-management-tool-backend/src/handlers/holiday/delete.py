from src.database import db
from src.models import Holiday

class HolidayDeleteHandler:

    def __init__(self):
        self.session = db.session()

    def delete(self, request):
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

            self.session.delete(holiday)
            self.session.commit()

            return {
                "status": True,
                "error": 0,
                "message": "Holiday deleted successfully",
                "data": {
                    "holiday_id": holiday_id
                }
            }

        except Exception as e:
            self.session.rollback()
            return {
                "status": False,
                "error": 1,
                "message": f"Holiday deletion failed due to {e}",
                "data": {}
            }
