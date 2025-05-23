from flask import Blueprint, request
from src.handlers import TimesheetList, CreateTimesheet , UpdateTimesheet ,SingleTimesheet ,DeleteTimesheet ,TimesheetListAll


timesheet_blueprint = Blueprint("timesheet", __name__)


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

@timesheet_blueprint.route("/get-all-list", methods = ["POST"])
def get_all_timesheet():
    return TimesheetListAll().listAll(request=request)