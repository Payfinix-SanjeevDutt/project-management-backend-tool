from .stages import stage_blueprint
from .tasks import task_blueprint
from .project import project_Blueprint
from .employee import employee_blueprint
from .auth import auth_blueprint
from .sprints import sprint_blueprint
from .attachment import attachment_blueprint
from .timesheet import timesheet_blueprint
from .timelog import timelog_blueprint
from .email_notification import email_notification_blueprint

def register_blueprints(app):
    app.register_blueprint(auth_blueprint, url_prefix="/auth")  
    app.register_blueprint(employee_blueprint, url_prefix="/employee")  
    app.register_blueprint(project_Blueprint, url_prefix="/project")
    app.register_blueprint(stage_blueprint, url_prefix="/stage")
    app.register_blueprint(task_blueprint,  url_prefix="/task")
    app.register_blueprint(sprint_blueprint, url_prefix="/sprint")
    app.register_blueprint(attachment_blueprint, url_prefix="/attachment")
    app.register_blueprint(timesheet_blueprint, url_prefix="/timesheet")
    app.register_blueprint(timelog_blueprint,url_prefix="/timelog")
    app.register_blueprint(email_notification_blueprint,url_prefix="/email_notification")
    