from flask import Blueprint, request
from src.handlers import CreateLeave
from src.handlers import LeaveDeleteHandler ,LeaveListHandler ,ApplyLeave,AssignLeave,Create_Policy

leave_blueprint = Blueprint("leave", __name__)

@leave_blueprint.route("/create-leave", methods=["POST"])
def create_leave():
    return CreateLeave().create(request=request)

@leave_blueprint.route("/delete-leave", methods=["POST"])
def delete_leave():
    return LeaveDeleteHandler().delete(request=request)


@leave_blueprint.route("/create-policy", methods=["POST"])
def createpolicy():
    return Create_Policy().create_policy(request=request)

@leave_blueprint.route("/leave-assign", methods=["POST"])
def assignleave():
    return AssignLeave().assign_leave_balance(request=request)

@leave_blueprint.route("/list-leave", methods=["GET"])
def list_leave2():
    return AssignLeave().get_all_leave_balances()

@leave_blueprint.route("/apply-leave", methods=["POST"])
def applyLeave():
    return ApplyLeave().apply_leave(request=request)

@leave_blueprint.route("/list-all-leave", methods=["GET"])
def get_all_leaves():
    limit = request.args.get('limit', 50)
    offset = request.args.get('offset', 0)
    handler = LeaveListHandler()
    return handler.get_all_leaves(limit=int(limit), offset=int(offset))

@leave_blueprint.route("/list-employee-leave", methods=["POST"])
def list_employee_leave():
    return LeaveListHandler().get_leaves_by_employee(request=request)