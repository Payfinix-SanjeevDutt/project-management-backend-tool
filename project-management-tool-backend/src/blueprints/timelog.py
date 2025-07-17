from flask import Blueprint,request
from src.handlers import CreateTimeLog , GetTimeLog ,UpdateTimeLog,GetEmpDetailsByMonth,GetEmpDetailsByDate ,FaceVerify,GetTimeLogWeekly

timelog_blueprint = Blueprint("timelog",__name__)

@timelog_blueprint.route("/create",methods = ["POST"])
def create_timelog():
    return CreateTimeLog().create(request=request)

@timelog_blueprint.route("/list",methods = ["POST"])
def get_timelog():
    return GetTimeLog().fetch(request=request)

@timelog_blueprint.route("/list/weekly",methods = ["POST"])
def get_timelog_weekly():
    return GetTimeLogWeekly().fetchweekly(request=request)

@timelog_blueprint.route("/update",methods = ["POST"])
def update_timelog():
    return UpdateTimeLog().update(request=request)

@timelog_blueprint.route("/getdaily",methods = ["POST"])
def daily_timelog():
    return GetEmpDetailsByDate().emp_details_date(request=request)

@timelog_blueprint.route("/monthly",methods = ["POST"])
def monthly_timelog():
    return GetEmpDetailsByMonth().emp_details_month(request=request)


@timelog_blueprint.route("/face-verify",methods = ["POST"])
def face_verify():
    fv = FaceVerify()
    return fv.verify_face(request=request)