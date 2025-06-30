from src.database import db
from src.models import Holiday
from src.utils import generate_unique_key

class HolidayCreateHandler:

    def __init__(self):
        self.session = db.session()

    def create(self, request):
        try:
            body = request.json

            holiday_id = generate_unique_key()
            holiday_object = Holiday(
                holiday_id=holiday_id,
                holiday_name=body['holiday_name'],
                start_date=body['start_date'],
                end_date=body['end_date'],
                is_optional=body.get('is_optional'),
                type=body.get('type')
            )


            self.session.add(holiday_object)
            self.session.commit()

            return {
                "status": True,
                "error": 0,
                "message": "Holiday created successfully",
                "data": {
                    "holiday_name": holiday_object.holiday_name,
                    "holiday_id": holiday_object.holiday_id
                }
            }

        except Exception as e:
            self.session.rollback()
            return {
                "status": False,
                "error": 1,
                "message": f"Holiday creation failed due to {e}",
                "data": {
                    "holiday_name": '',
                    "holiday_id": ''
                }
            }
