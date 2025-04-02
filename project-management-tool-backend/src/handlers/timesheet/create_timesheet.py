from src.database import db
from src.models import Timesheet


class CreateTimesheet:

    def __init__(self):
        self.session = db.session()

    def create(self, request):
        try:
            body = request.json

            timesheets = body if isinstance(body, list) else [body]

            created_timesheets = []

            for entry in timesheets:
                timesheet_object = Timesheet(
                    projectName=entry['project_name'],
                    employee_id=entry['employee_id'],
                    jobName=entry['job_name'],
                    workItem=entry['work_item'],
                    description=entry['description'],
                    totalHours=entry['total_hours'],
                    startDate=entry['startDate'],
                    billable_status=entry['billable_status']
                )

                self.session.add(timesheet_object)
                self.session.flush()  

                created_timesheets.append({
                    "timesheet_id": timesheet_object.timesheet_id,
                    "project_name": timesheet_object.projectName
                })

            self.session.commit()

            return {
                "status": True,
                "error": 0,
                "message": "Timesheets created successfully",
                "data": created_timesheets
            }

        except Exception as e:
            self.session.rollback()  
            return {
                "status": False,
                "error": 1,
                "message": f"Timesheet creation unsuccessful due to {e}",
                "data": []
            }
