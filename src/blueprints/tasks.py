from flask import Blueprint, request

from src.handlers import TaskCreateHandler,TaskDeleteHandler,AllTaskHandler,TaskUpdateHandler,TaskSingleHandler ,AllTaskDeleteHandler ,CommentHandler,EmployeeTaskReport

from src.handlers.tasks.task_mail_invite import SendInvite

task_blueprint = Blueprint("task", __name__)

@task_blueprint.route("/create-task", methods=['POST'])
def stage_create():
    return TaskCreateHandler().create(request=request)

@task_blueprint.route("/delete-task", methods=['DELETE'])
def stage_delete():
    return TaskDeleteHandler().delete(request=request)

@task_blueprint.route("/get-all-tasks", methods=['GET'])
def stage_read_all():
    return AllTaskHandler().get_all_tasks(request=request)

@task_blueprint.route("/list_sprint_tasks", methods=['POST'])
def task_list():
    print(request)
    return AllTaskHandler().get_sprint_task(request=request)

@task_blueprint.route("/updatetask", methods=['POST'])
def stage_update():
    return TaskUpdateHandler().update_task(request=request)

@task_blueprint.route("/getsingletask", methods=['POST'])
def stage_read():
    return TaskSingleHandler().get_single_task(request=request)

@task_blueprint.route("/delete-all-task", methods=['DELETE'])
def stage_delete_all():
    return AllTaskDeleteHandler().delete_all(request=request)

@task_blueprint.route("/comments", methods= ['GET','POST'])
def task_comment():
    return CommentHandler().process_data()

@task_blueprint.route('/history', methods=['GET'])
def task_history():
    return CommentHandler().get_history(request=request)

@task_blueprint.route('/actions', methods=['POST'])
def task_actions():
    return CommentHandler().perform_action(request=request)

@task_blueprint.route('/employee-task-report', methods=['POST'])
def employee_task_report():
    return EmployeeTaskReport().get_employee_task_report(request=request)

@task_blueprint.route('/assignee',methods=['POST'])
def mail_assignee():
    return SendInvite(request=request).send_assignee_notification()


@task_blueprint.route('/reporter',methods=['POST'])
def mail_reporter():
    return SendInvite(request=request).send_reporter_notification()
