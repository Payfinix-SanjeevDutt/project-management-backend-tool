from flask import Blueprint,request
from src.handlers import CreateTimeLog , GetTimeLog ,UpdateTimeLog

timelog_blueprint = Blueprint("timelog",__name__)

@timelog_blueprint.route("/create",methods = ["POST"])
def create_timelog():
    return CreateTimeLog().create(request=request)

@timelog_blueprint.route("/list",methods = ["POST"])
def get_timelog():
    return GetTimeLog().fetch(request=request)


@timelog_blueprint.route("/update",methods = ["POST"])
def update_timelog():
    return UpdateTimeLog().update(request=request)

@timelog_blueprint.route("/update-timelog",methods = ["POST"])
def update_timelog2():
    return UpdateTimeLog().update(request=request)