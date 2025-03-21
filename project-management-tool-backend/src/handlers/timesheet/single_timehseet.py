from src.database import db
from sqlalchemy import select
from src.models import Timesheet, Employee

class SingleTimesheet:
    def __init__(self):
        self.db = db.session()

    def get_single_timesheet(self, request):
        try:
            body = request.json
            timesheet_id = body.get("timesheet_id")
            employee_id = body.get("employee_id")

            if not timesheet_id or not employee_id:
                return {
                    "status": False,
                    "error_code": 1,
                    "message": "Timesheet ID and Employee ID are required",
                    "data": None
                }

            query = (
                select(
                    Timesheet.timesheet_id,
                    Timesheet.projectName,
                    Timesheet.jobName,
                    Timesheet.workItem,
                    Timesheet.description,
                    Timesheet.billable_status,
                    Timesheet.startDate,
                    Timesheet.totalHours,
                    Employee.name,
                    Employee.email,
                    Employee.avatar
                )
                .outerjoin(Employee, Timesheet.employee_id == Employee.employee_id)
                .where(
                    (Timesheet.timesheet_id == timesheet_id) & 
                    (Timesheet.employee_id == employee_id)
                )
            )

            result = self.db.execute(query).first()

            if not result:
                return {
                    "status": False,
                    "error_code": 2,
                    "message": "No matching timesheet found",
                    "data": None
                }

            timesheet_data = {
                "timesheet_id": result.timesheet_id,
                "project_name": result.projectName,
                "job_name": result.jobName,
                "work_item": result.workItem,
                "description": result.description,
                "billable_status": result.billable_status,
                "startDate": result.startDate,
                "employee_name": result.name,
                "avatar": result.avatar,
                "total_hours": result.totalHours.strftime("%H:%M:%S") if result.totalHours else "00:00:00",
            }

            return {
                "status": True,
                "error_code": 0,
                "message": "Timesheet fetched successfully",
                "data": timesheet_data
            }

        except Exception as e:
            print(e)
            return {
                "status": False,
                "error_code": 3,
                "message": f"Failed: {str(e)}",
                "data": None
            }
