from src.database import db
from src.models import Holiday

class HolidayDeleteALLHandler:

    def __init__(self):
        self.session = db.session()

   

    def deleteall(self, request):
        try:
            body = request.get_json()
            holiday_ids = body.get('holiday_ids')

            if not holiday_ids or not isinstance(holiday_ids, list):
                return {
                    "status": False,
                    "error": 1,
                    "message": "holiday_ids (list) is required",
                    "data": {}
                }

            # Query all holidays that match the IDs
            holidays = self.session.query(Holiday).filter(Holiday.holiday_id.in_(holiday_ids)).all()

            if not holidays:
                return {
                    "status": False,
                    "error": 1,
                    "message": "No holidays found to delete",
                    "data": {}
                }

            # Delete all found holidays
            for holiday in holidays:
                self.session.delete(holiday)

            self.session.commit()

            return {
                "status": True,
                "error": 0,
                "message": f"{len(holidays)} holidays deleted successfully",
                "data": {
                    "deleted_ids": [h.holiday_id for h in holidays]
                }
            }

        except Exception as e:
            self.session.rollback()
            return {
                "status": False,
                "error": 1,
                "message": f"Bulk deletion failed due to {e}",
                "data": {}
            }
