from src.database import db
from sqlalchemy import select
from src.models import Timesheet, Employee

class TimesheetList:
    def __init__(self):
        self.db = db.session()

    def list(self,request):
        try:
            body = request.json

            query = select(
                Timesheet.timesheet_id,
                Timesheet.projectName,
                Timesheet.jobName,
                Timesheet.workItem,
                Timesheet.description,
                # Timesheet.totalHours,
                Timesheet.billable_status,
                Timesheet.startDate,
                Employee.name,
                Employee.email,
                Employee.avatar
            ).join(Employee, Timesheet.employee_id == body['employee_id'])
            

            result = self.db.execute(query).all()
            response = []

            for item in result: 
                response.append({
                    "timesheet_id": item.timesheet_id,
                    "project_name": item.projectName,
                    "job_name": item.jobName,
                    "work_item": item.workItem,
                    "description": item.description,
                    # "total_hours": item.totalHours,
                    "billable_status": item.billable_status,  # Make sure this field exists in your SQL query
                    "startDate": item.startDate # Make sure this is a valid field
                })

            return {
                "status": True,
                "error_code": 0,
                "message": 'Timesheet fetched successfully',
                "data": response
            }

        except Exception as e:
            print(e)
            return {
                "status": False,
                "error_code": 1,
                "message": f'Failed {e}',
                "data": []
            }
