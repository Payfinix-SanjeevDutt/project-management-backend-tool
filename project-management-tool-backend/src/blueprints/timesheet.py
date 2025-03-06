from flask import Blueprint, request
from src.handlers import TimesheetList, CreateTimesheet


timesheet_blueprint = Blueprint("blueprint", __name__)



@timesheet_blueprint.route("/list", methods=["POST"])
def list_timesheet():
    return TimesheetList().list(request=request)


@timesheet_blueprint.route("/create", methods=["POST"])
def create_timesheet():
    return CreateTimesheet().create(request=request)


# @timesheet_blueprint.route("/delete" , methods = ['DELETE'])
# def delete_timesheet():
#     # return DeleteProject(request=request).delete()

# @timesheet_blueprint.route("/update", methods=['POST'])
# def update_timesheet():
#     # return UpdateProject(request=request).update()