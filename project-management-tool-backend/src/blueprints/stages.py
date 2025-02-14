from flask import Blueprint, request

from src.handlers import StageCreateHandler,StageDeleteHandler,StageUpdateHandler,StageSingleHandler,AllStageHandler,EmployeeStageReport

stage_blueprint = Blueprint("stage", __name__)

@stage_blueprint.route("/create-stage", methods=['POST'])
def stage_create():
    return StageCreateHandler().create(request=request)

@stage_blueprint.route("/getstage", methods=['POST'])
def stage_read():
    return StageSingleHandler().get_single_stage(request=request)

@stage_blueprint.route("/get-all-stages", methods=['POST'])
def stage_read_all():
    return AllStageHandler().get_all_stage(request=request)

@stage_blueprint.route("/update-stage", methods=['PUT'])
def stage_update():
    return StageUpdateHandler().stage_update(request=request)

@stage_blueprint.route("/delete-stage", methods=['DELETE'])
def stage_delete():
    return StageDeleteHandler().delete_stage(request=request)

@stage_blueprint.route("/stage-employee-report", methods=['POST'])
def stage_employeereport():
    return EmployeeStageReport().get_stage_employee_report(request = request)