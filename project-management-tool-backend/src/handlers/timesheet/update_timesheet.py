from src.database import db
from src.models import Timesheet

class UpdateTimesheet:

    def __init__(self):
        self.session = db.session()

    def update(self, request):
        try:
            body = request.json
            timesheet_id = body.get("timesheet_id")

            if not timesheet_id:
                return {
                    "status": False,
                    "error": 1,
                    "message": "Missing timesheet_id in request body",
                    "data": {}
                }

            timesheet_object = self.session.query(Timesheet).filter_by(timesheet_id=timesheet_id).first()
            
            if not timesheet_object:
                return {
                    "status": False,
                    "error": 1,
                    "message": "Timesheet not found",
                    "data": {}
                }

            timesheet_object.projectName = body.get('project_name', timesheet_object.projectName)
            timesheet_object.employee_id = body.get('employee_id', timesheet_object.employee_id)
            timesheet_object.jobName = body.get('job_name', timesheet_object.jobName)
            timesheet_object.workItem = body.get('work_item', timesheet_object.workItem)
            timesheet_object.description = body.get('description', timesheet_object.description)
            timesheet_object.totalHours = body.get('total_hours', timesheet_object.totalHours)
            timesheet_object.startDate = body.get('startDate', timesheet_object.startDate)
            timesheet_object.billable_status = body.get('billable_status', timesheet_object.billable_status)

            self.session.commit()
            return {
                "status": True,
                "error": 0,
                "message": "Timesheet updated successfully",
                "data": {
                    "timesheet_id": timesheet_object.timesheet_id,
                    "project_name": timesheet_object.projectName
                }
            }
        except Exception as e:
            self.session.rollback()
            return {
                "status": False,
                "error": 1,
                "message": f"Timesheet update unsuccessful due to {e}",
                "data": {}
            }
