# # routes/leave_policy.py
# from flask import Blueprint, request, jsonify
# from src.models import LeavePolicy
# from src.database import db


# class Create_Policy:
#     def __init__(self):
#         self.session = db.session()
        
#     def create_policy(self, request):
#         data = request.json
#         leave_type = data.get("leave_type")
#         default_days = data.get("default_days")
#         if not leave_type or default_days is None:
#             return jsonify({"error": "Missing required fields"}), 400

#         if LeavePolicy.query.filter_by(leave_type=leave_type).first():
#             return jsonify({"error": "Leave type already exists"}), 409

#         policy = LeavePolicy(leave_type=leave_type, default_days=default_days)
#         db.session.add(policy)
#         db.session.commit()
#         return jsonify({"message": "Leave policy created"}), 201

from flask import Blueprint, request, jsonify
from src.models import LeavePolicy
from src.database import db

class Create_Policy:
    def __init__(self):
        self.session = db.session()

    def create_policy(self,request):
        data = request.json
        policies = data.get("policies")

        if not policies or not isinstance(policies, list):
            return jsonify({"error": "Invalid data format"}), 400

        for policy in policies:
            leave_type = policy.get("leave_type")
            default_days = policy.get("default_days")

            if not leave_type or default_days is None:
                return jsonify({"error": "Each policy must have leave_type and default_days"}), 400

            existing_policy = LeavePolicy.query.filter_by(leave_type=leave_type).first()

            if existing_policy:
                existing_policy.default_days = default_days  # Update
            else:
                new_policy = LeavePolicy(leave_type=leave_type, default_days=default_days)
                db.session.add(new_policy)

        db.session.commit()
        return jsonify({"message": "Leave settings saved successfully"}), 200
