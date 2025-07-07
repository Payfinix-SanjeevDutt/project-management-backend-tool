from src.database import db
from src.models import Leave, Employee
from sqlalchemy.orm import joinedload
from flask import request
import time

class LeaveListHandler:

    def __init__(self):
        self.session = db.session()

    def get_all_leaves(self, limit=50, offset=0):
        try:
            start_total = time.time()

            start_db = time.time()
            leaves = (
                self.session.query(Leave)
                .options(joinedload(Leave.employee))
                .order_by(Leave.start_date.desc())
                .offset(offset)
                .limit(limit)
                .all()
            )
            print(f"[DEBUG] Query time (all): {time.time() - start_db:.2f}s")

            # Serialize
            start_serial = time.time()
            data = [self.serialize_leave(leave) for leave in leaves]
            print(f"[DEBUG] Serialization time: {time.time() - start_serial:.2f}s")
            print(f"[DEBUG] Total handler time: {time.time() - start_total:.2f}s")

            return {
                "status": True,
                "error": 0,
                "message": "All leave records fetched successfully.",
                "data": data
            }

        except Exception as e:
            return {
                "status": False,
                "error": 1,
                "message": f"Failed to fetch all leaves: {str(e)}",
                "data": []
            }

    def get_leaves_by_employee(self, request):
        try:
            start_total = time.time()
            body = request.get_json() or {}

            employee_id = body.get("employee_id")
            if not employee_id:
                return {
                    "status": False,
                    "error": 1,
                    "message": "Missing 'employee_id' in request body.",
                    "data": []
                }

            limit = int(body.get("limit", 50))
            offset = int(body.get("offset", 0))

            start_db = time.time()
            leaves = (
                self.session.query(Leave)
                .options(joinedload(Leave.employee))
                .filter(Leave.employee_id == employee_id)
                .order_by(Leave.start_date.desc())
                .offset(offset)
                .limit(limit)
                .all()
            )
            print(f"[DEBUG] Query time (by employee): {time.time() - start_db:.2f}s")

            start_serial = time.time()
            data = [self.serialize_leave(leave) for leave in leaves]
            print(f"[DEBUG] Serialization time: {time.time() - start_serial:.2f}s")
            print(f"[DEBUG] Total handler time: {time.time() - start_total:.2f}s")

            return {
                "status": True,
                "error": 0,
                "message": f"Leaves fetched for employee ID {employee_id}.",
                "data": data
            }

        except Exception as e:
            return {
                "status": False,
                "error": 1,
                "message": f"Failed to fetch leaves by employee: {str(e)}",
                "data": []
            }

    def serialize_leave(self, leave):
        return {
            "leave_id": leave.leave_id,
            "employee_id": leave.employee_id,
            "employee_name": leave.employee.name if leave.employee else "Unknown",
            "leave_type": leave.leave_type,
            "start_date": str(leave.start_date),
            "end_date": str(leave.end_date),
            "is_half_day": leave.is_half_day,
            "reason": leave.reason,
            "applied_on": str(leave.applied_on),
            "emp_avatar": leave.employee.avatar if leave.employee else None
        }
