from src.database import db
from src.models import Timesheet
from sqlalchemy.exc import SQLAlchemyError

class DeleteTimesheet:
    def __init__(self):
        self.db = db.session()

    def delete(self, request):
        try:
            body = request.json
            timesheet_id = body.get("timesheet_id")
            employee_id = body.get("employee_id")

            if not timesheet_id or not employee_id:
                return {
                    "status": False,
                    "error_code": 1,
                    "message": "Timesheet ID and Employee ID are required",
                }

            timesheet = (
                self.db.query(Timesheet)
                .filter(Timesheet.timesheet_id == timesheet_id, Timesheet.employee_id == employee_id)
                .first()
            )

            if not timesheet:
                return {
                    "status": False,
                    "error_code": 2,
                    "message": "Timesheet not found",
                }

            self.db.delete(timesheet)
            self.db.commit()

            return {
                "status": True,
                "error_code": 0,
                "message": "Timesheet deleted successfully",
            }

        except SQLAlchemyError as e:
            self.db.rollback() 
            print(e)
            return {
                "status": False,
                "error_code": 3,
                "message": f"Database error: {str(e)}",
            }

        except Exception as e:
            print(e)
            return {
                "status": False,
                "error_code": 4,
                "message": f"Failed: {str(e)}",
            }
