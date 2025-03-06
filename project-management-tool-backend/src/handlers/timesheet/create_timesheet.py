from src.database import db
from src.models import Timesheet

class CreateTimesheet:

    def __init__(self):
        self.session = db.session()

    def create(self, request):
        try:
            body = request.json

            timesheet_object = Timesheet(
                projectName=body['project_name'],
                employee_id=body['employee_id'],
                jobName=body['job_name'],
                workItem=body['work_item'],
                description=body['description'],
                totalHours=body['total_hours']
            )

            self.session.add(timesheet_object)
            self.session.commit()
            return {
                "status": True,
                "error": 0,
                "message": "Timesheet created successfully",
                "data": {
                    "timesheet_id": timesheet_object.timesheet_id,
                    "project_name": timesheet_object.projectName
                }
            }
        except Exception as e:
            return {
                "status": False,
                "error": 1,
                "message":f"Timesheet creation unsuccessful due to {e}",
                "data": {
                    "timesheet_id": '',
                    "project_name": ''
                }
            }
