from flask import Blueprint, request
from src.handlers import HolidayCreateHandler,HolidayListHandler, HolidayDeleteHandler, HolidayGetHandler, HolidayUpdateHandler ,HolidayDeleteALLHandler



holiday_blueprint = Blueprint("holiday", __name__)

@holiday_blueprint.route("/create-holiday", methods=["POST"])
def create_holiday():
    return HolidayCreateHandler().create(request=request)


@holiday_blueprint.route("/list-holidays", methods=["GET"])
def list_holidays():
    return HolidayListHandler().list()


@holiday_blueprint.route("/delete-holiday", methods=["POST"])
def delete_holiday():
    return HolidayDeleteHandler().delete(request)

@holiday_blueprint.route("/delete-holidays", methods=["POST"])
def delete_all_holiday():
    return HolidayDeleteALLHandler().deleteall(request)


@holiday_blueprint.route("/get-holiday", methods=["POST"])
def get_holiday():
    return HolidayGetHandler().get(request)


@holiday_blueprint.route("/update-holiday", methods=["PUT"])
def update_holiday():
    return HolidayUpdateHandler().update(request)