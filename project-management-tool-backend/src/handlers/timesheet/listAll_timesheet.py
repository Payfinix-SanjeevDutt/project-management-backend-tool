from collections import defaultdict
from src.database import db
from sqlalchemy import select
from src.models import Timesheet, Employee
from datetime import datetime
from flask import request  

class TimesheetListAll:
    def __init__(self):
        self.db = db.session()

    def listAll(self,request):
        try:
            data = request.get_json()
            start_date = data.get('start_date')
            end_date = data.get('end_date')

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
                    Employee.employee_id,
                    Employee.name,
                    Employee.avatar
                )
                .outerjoin(Employee, Timesheet.employee_id == Employee.employee_id)
            )

            if start_date and end_date:
                start = datetime.strptime(start_date, "%Y-%m-%d")
                end = datetime.strptime(end_date, "%Y-%m-%d")
                query = query.where(Timesheet.startDate.between(start, end))

            result = self.db.execute(query).all()
            grouped_data = {}

            for item in result:
                emp_id = item.employee_id
                date_str = item.startDate.strftime("%Y-%m-%d") if item.startDate else "Unknown Date"

                if emp_id not in grouped_data:
                    grouped_data[emp_id] = {
                        "employee_name": item.name,
                        "employee_id": emp_id,
                        "avatar": item.avatar,
                        "billable_status": item.billable_status,
                        "description": item.description,
                        "job_name": item.jobName,
                        "project_name": item.projectName,
                        "timesheet_id": item.timesheet_id,
                        "days": {}
                    }

                if date_str not in grouped_data[emp_id]["days"]:
                    grouped_data[emp_id]["days"][date_str] = []

                grouped_data[emp_id]["days"][date_str].append({
                    "work_item": item.workItem,
                    "total_hours": item.totalHours.strftime("%H:%M") if item.totalHours else "00:00"
                })

            response = list(grouped_data.values())

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
