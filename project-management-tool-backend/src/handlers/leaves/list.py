# src/handlers/leave_list_handler.py

from src.database import db
from src.models import Leave, Employee
from sqlalchemy.orm import joinedload
from flask import request  # assuming Flask
import time

class LeaveListHandler:
    
    def __init__(self):
        self.session = db.session()

    def list(self, request):
        try:
            start_total = time.time()

            limit = int(request.args.get("limit", 50))
            offset = int(request.args.get("offset", 0))

            # Measure DB query time
            start_db = time.time()
            leaves = (
                self.session.query(Leave)
                .options(joinedload(Leave.employee))
                .order_by(Leave.start_date.desc())
                .offset(offset)
                .limit(limit)
                .all()
            )
            print(f"[DEBUG] Query time: {time.time() - start_db:.2f}s")

            # Measure serialization time
            start_serial = time.time()
            data = [{
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
            } for leave in leaves]
            print(f"[DEBUG] Serialization time: {time.time() - start_serial:.2f}s")

            print(f"[DEBUG] Total handler time: {time.time() - start_total:.2f}s")

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