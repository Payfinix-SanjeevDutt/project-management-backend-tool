from src.database import db
from sqlalchemy import select
from src.models import Timesheet, Employee

class TimesheetList:
    def __init__(self):
        self.db = db.session()

    def list(self, request):
        try:
            body = request.json
            employee_id = body.get("employee_id") 

            if not employee_id:
                return {
                    "status": False,
                    "error_code": 1,
                    "message": "Employee ID is required",
                    "data": []
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
                .where(Timesheet.employee_id == employee_id) 
            )

            result = self.db.execute(query).all()
            response = []

            for item in result:
                response.append({
                    "timesheet_id": item.timesheet_id,
                    "project_name": item.projectName,
                    "job_name": item.jobName,
                    "work_item": item.workItem,
                    "description": item.description,
                    "billable_status": item.billable_status,
                    "startDate": item.startDate,
                    "employee_name": item.name,
                    "avatar": item.avatar,
                    "total_hours": item.totalHours.strftime("%H:%M:%S") if item.totalHours else "00:00:00",

                })

            return {
                "status": True,
                "error_code": 0,
                "message": "Timesheet fetched successfully",
                "data": response
            }

        except Exception as e:
            print(e)
            return {
                "status": False,
                "error_code": 1,
                "message": f"Failed {e}",
                "data": []
            }
