from flask import Blueprint, request

from src.handlers import SprintCreateHandler, SprintUpdateHandler, SprintDeleteHandler,SprintListHandler

sprint_blueprint = Blueprint("sprint", __name__)

@sprint_blueprint.route("/createsprint", methods=['POST'])
def sprint_create():
    return SprintCreateHandler().create(request=request)

@sprint_blueprint.route("/updatesprint", methods=['PUT'])
def sprint_update():
    return SprintUpdateHandler().sprint_update(request=request)

@sprint_blueprint.route("/updatesprintdates", methods=['PUT'])
def sprint_update_dates():
    return SprintUpdateHandler().update_sprint_dates(request=request)

@sprint_blueprint.route("/deletesprint", methods=['DELETE'])
def sprint_delete():
    return SprintDeleteHandler().delete_sprint(request=request)

@sprint_blueprint.route("/listsprint", methods=['POST'])
def sprint_list():
    return SprintListHandler().list_sprint(request=request)