from flask import Blueprint, request, jsonify
from src.models import LeaveBalance, LeavePolicy
from src.models import Employee , Leave
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
        try:
            excluded_ids = ['ELKHGFJJKEHLKJG4102836', 'Nischal0001']
 
            records = (
                db.session.query(Employee, LeaveBalance)
                .outerjoin(LeaveBalance, Employee.employee_id == LeaveBalance.employee_id)
                .filter(~Employee.employee_id.in_(excluded_ids))
                .all()
            )
 
            result = {}
 
            for employee, balance in records:
                emp_bal = result.setdefault(employee.employee_id, [])
 
                if balance:
                    emp_bal.append({
                        "emp_name": employee.name,
                        "emp_avatar": employee.avatar,
                        "leave_type": balance.leave_type,
                        "balance": balance.balance
                    })
                else:
                    # If no balance, still add a placeholder so frontend doesn't break
                    emp_bal.append({
                        "emp_name": employee.name,
                        "emp_avatar": employee.avatar,
                        "leave_type": None,
                        "balance": 0
                    })
 
            return jsonify(result), 200
 
        except Exception as e:
            return jsonify({"error": f"Failed to fetch leave balances: {str(e)}"}), 500
 
 
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
 
    def get_leave_history(self):
        employee_id = request.args.get("employee_id")
        leave_type = request.args.get("leave_type")
 
        if not employee_id or not leave_type:
            return jsonify({"error": "employee_id and leave_type are required"}), 400
 
        leaves = Leave.query.filter_by(employee_id=employee_id, leave_type=leave_type).order_by(Leave.start_date.desc()).all()
 
        return jsonify([
            {
                "start_date": leave.start_date.strftime("%Y-%m-%d"),
                "end_date": leave.end_date.strftime("%Y-%m-%d"),
                "leave_type": leave.leave_type,
                "reason": leave.reason
            }
            for leave in leaves
        ]), 200
 

# from flask import Blueprint, request, jsonify
# from src.models import LeaveBalance, LeavePolicy
# from src.models import Employee , Leave
# from src.database import db
# from sqlalchemy import select

# class AssignLeave:
#     def __init__(self):
#         self.session = db.session()
        
#     def assign_leave_balance(self, request):
#         body = request.json
#         employee_ids = body.get("employee_ids")

#         if not employee_ids or not isinstance(employee_ids, list):
#             return jsonify({"error": "employee_ids must be a non-empty list"}), 400

#         policies = LeavePolicy.query.all()

#         for emp_id in employee_ids:
#             employee = Employee.query.filter_by(employee_id=emp_id).first()
#             if not employee:
#                 continue  # Optionally log missing employee

#             # Remove existing balances
#             LeaveBalance.query.filter_by(employee_id=emp_id).delete()

#             # Assign new balances from current policies
#             for policy in policies:
#                 db.session.add(LeaveBalance(
#                     employee_id=emp_id,
#                     leave_type=policy.leave_type,
#                     balance=policy.default_days
#                 ))

#         db.session.commit()
#         return jsonify({"message": "Leave balances assigned to all valid employees"}), 200


#     def get_all_leave_balances(self):
#         try:
#             excluded_ids = ['ELKHGFJJKEHLKJG4102836', 'Nischal0001']

#             records = (
#                 db.session.query(Employee, LeaveBalance)
#                 .outerjoin(LeaveBalance, Employee.employee_id == LeaveBalance.employee_id)
#                 .filter(~Employee.employee_id.in_(excluded_ids))
#                 .all()
#             )

#             result = {}

#             for employee, balance in records:
#                 emp_bal = result.setdefault(employee.employee_id, [])

#                 if balance:
#                     emp_bal.append({
#                         "emp_name": employee.name,
#                         "emp_avatar": employee.avatar,
#                         "leave_type": balance.leave_type,
#                         "balance": balance.balance
#                     })
#                 else:
#                     # If no balance, still add a placeholder so frontend doesn't break
#                     emp_bal.append({
#                         "emp_name": employee.name,
#                         "emp_avatar": employee.avatar,
#                         "leave_type": None,
#                         "balance": 0
#                     })

#             return jsonify(result), 200

#         except Exception as e:
#             return jsonify({"error": f"Failed to fetch leave balances: {str(e)}"}), 500


#     def get_leave_balance_post(self, request):
#         data = request.json
#         employee_id = data.get("employee_id")

#         if not employee_id:
#             return jsonify({"error": "employee_id is required"}), 400

#         balances = LeaveBalance.query.filter_by(employee_id=employee_id).all()
#         if not balances:
#             return jsonify({"error": "No balances found"}), 404

#         return jsonify([
#             {"leave_type": b.leave_type, "balance": b.balance}
#             for b in balances
#         ]), 200

#     def get_leave_history(self):
#         employee_id = request.args.get("employee_id")
#         leave_type = request.args.get("leave_type")

#         if not employee_id or not leave_type:
#             return jsonify({"error": "employee_id and leave_type are required"}), 400

#         leaves = Leave.query.filter_by(employee_id=employee_id, leave_type=leave_type).order_by(Leave.start_date.desc()).all()

#         return jsonify([
#             {
#                 "start_date": leave.start_date.strftime("%Y-%m-%d"),
#                 "end_date": leave.end_date.strftime("%Y-%m-%d"),
#                 "leave_type": leave.leave_type,
#                 "reason": leave.reason
#             }
#             for leave in leaves
#         ]), 200