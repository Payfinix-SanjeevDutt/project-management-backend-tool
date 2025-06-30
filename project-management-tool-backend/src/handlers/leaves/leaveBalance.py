from flask import Blueprint, request, jsonify
from src.models import LeaveBalance, LeavePolicy
from src.models import Employee
from src.database import db
from sqlalchemy import select

class AssignLeave:
    def __init__(self):
        self.session = db.session()
        
    def assign_leave_balance(self, request):
        body = request.json
        employee_ids = body.get("employee_ids")

        if not employee_ids or not isinstance(employee_ids, list):
            return jsonify({"error": "employee_ids must be a non-empty list"}), 400

        policies = LeavePolicy.query.all()

        for emp_id in employee_ids:
            employee = Employee.query.filter_by(employee_id=emp_id).first()
            if not employee:
                continue  # Optionally log missing employee

            # Remove existing balances
            LeaveBalance.query.filter_by(employee_id=emp_id).delete()

            # Assign new balances from current policies
            for policy in policies:
                db.session.add(LeaveBalance(
                    employee_id=emp_id,
                    leave_type=policy.leave_type,
                    balance=policy.default_days
                ))

        db.session.commit()
        return jsonify({"message": "Leave balances assigned to all valid employees"}), 200


    def get_all_leave_balances(self):
        balances = LeaveBalance.query.all()
        if not balances:
            return jsonify({"error": "No balances found"}), 404

        result = {}
        for balance in balances:
            emp_bal = result.setdefault(balance.employee_id, [])
            # emp_name = select(Employee.name).outerjoin(Employee,balance.employee_id == Employee.employee_id),
            employee = Employee.query.filter_by(employee_id=balance.employee_id).first()
            emp_name = employee.name 
            emp_avatar = employee.avatar
            emp_bal.append({
                "emp_name" : emp_name,
                "emp_avatar" : emp_avatar,
                "leave_type": balance.leave_type,
                "balance": balance.balance
            })

        return jsonify(result), 200

    def get_leave_balance_post(self, request):
        data = request.json
        employee_id = data.get("employee_id")

        if not employee_id:
            return jsonify({"error": "employee_id is required"}), 400

        balances = LeaveBalance.query.filter_by(employee_id=employee_id).all()
        if not balances:
            return jsonify({"error": "No balances found"}), 404

        return jsonify([
            {"leave_type": b.leave_type, "balance": b.balance}
            for b in balances
        ]), 200
