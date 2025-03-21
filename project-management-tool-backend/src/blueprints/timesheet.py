from flask import Blueprint, request
from src.handlers import TimesheetList, CreateTimesheet , UpdateTimesheet ,SingleTimesheet ,DeleteTimesheet


timesheet_blueprint = Blueprint("blueprint", __name__)



@timesheet_blueprint.route("/list", methods=["POST"])
def list_timesheet():
    return TimesheetList().list(request=request)


@timesheet_blueprint.route("/create", methods=["POST"])
def create_timesheet():
    return CreateTimesheet().create(request=request)


@timesheet_blueprint.route("/delete" , methods = ['POST'])
def delete_timesheet():
    return DeleteTimesheet().delete(request=request)

@timesheet_blueprint.route("/update", methods=['POST'])
def update_timesheet():
    return UpdateTimesheet().update(request=request)

@timesheet_blueprint.route("/get-single-timesheet",methods = ['POST'])
def get_single_timesheet():
    return SingleTimesheet().get_single_timesheet(request=request)