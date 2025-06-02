from flask import Blueprint, request

from src.handlers import GetEmailNotification, EmailNotificationHandler,DeleteEmailNotification

email_notification_blueprint = Blueprint("email_notification",__name__)

@email_notification_blueprint.route("/",methods=['POST'])
def get_notifications_by_employee():
    return  GetEmailNotification(request=request).get_notifications_by_employee_id()

@email_notification_blueprint.route("/create", methods=['POST'])
def createEmailNotification():
    return EmailNotificationHandler(request=request).create_notification()

@email_notification_blueprint.route("/delete", methods=['DELETE'])
def deleteEmailNotification():
    return DeleteEmailNotification(request=request).delete()

