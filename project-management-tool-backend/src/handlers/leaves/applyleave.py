from flask import Blueprint, request, jsonify
from src.models import Leave, LeaveBalance, LeavePolicy
from src.utils import generate_unique_key
from src.database import db
from datetime import datetime

class ApplyLeave:
    def __init__(self):
        self.session = db.session()
        
    def apply_leave(self,request):
        data = request.json
        employee_id = data.get("employee_id")
        leave_type = data.get("leave_type")
        start_date = datetime.strptime(data.get("start_date"), "%Y-%m-%d").date()
        end_date = datetime.strptime(data.get("end_date"), "%Y-%m-%d").date()
        is_half_day = data.get("is_half_day", False)
        reason = data.get("reason", "")

        days_requested = 0.5 if is_half_day else (end_date - start_date).days + 1
        balance = LeaveBalance.query.filter_by(employee_id=employee_id, leave_type=leave_type).first()

        if not balance or balance.balance < days_requested:
            return jsonify({"error": "Insufficient leave balance"}), 400

        leave = Leave(
            leave_id=generate_unique_key(),
            employee_id=employee_id,
            leave_type=leave_type,
            start_date=start_date,
            end_date=end_date,
            is_half_day=is_half_day,
            reason=reason
        )

        db.session.add(leave)
        balance.balance -= days_requested
        db.session.commit()

        return jsonify({"message": "Leave applied successfully"}), 201