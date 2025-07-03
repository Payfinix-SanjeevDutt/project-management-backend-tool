# src/handlers/leave_list_handler.py

from src.database import db
from src.models import Leave, Employee


class LeaveListHandler:
    def __init__(self):
        self.session = db.session()

    def list(self, request):
        try:
            leaves = self.session.query(Leave).order_by(Leave.start_date.desc()).all()

            data = []
            for leave in leaves:
                employee = self.session.query(Employee).filter_by(employee_id=leave.employee_id).first()
                employee_name = employee.name if employee else "Unknown"

                data.append({
                    "leave_id": leave.leave_id,
                    "employee_id": leave.employee_id,
                    "employee_name": employee_name,
                    "leave_type": leave.leave_type,
                    "start_date": str(leave.start_date),
                    "end_date": str(leave.end_date),
                    "is_half_day": leave.is_half_day,
                    "reason": leave.reason,
                    "applied_on": str(leave.applied_on)
                })

            return {
                "status": True,
                "error": 0,
                "message": "Leave list fetched successfully.",
                "data": data
            }

        except Exception as e:
            return {
                "status": False,
                "error": 1,
                "message": f"Failed to fetch leave list: {str(e)}",
                "data": []
            }
