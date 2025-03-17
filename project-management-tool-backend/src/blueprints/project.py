from flask import Blueprint, request

from src.handlers import ListProject, CreateProject, UpdateProject, DisplayProject, CreateEmployeeUser ,SendInvite,DeleteProject,EmployeeTaskReport
from src.handlers import ListProjectUsers ,EmployeeProjectReport , DeleteProjectUsers, ProjectStagesReport, ProjectTaskReportStatusHandler

project_Blueprint = Blueprint("project",__name__)

@project_Blueprint.route("/list-projects", methods=["POST"])
def list_projects():
    return ListProject(request=request).list()

@project_Blueprint.route("/create-project", methods=["POST"])
def create_project():
    return CreateProject(request=request).create()

@project_Blueprint.route("/delete-project" , methods = ['DELETE'])
def delete_project():
    return DeleteProject(request=request).delete()

@project_Blueprint.route("/update-project", methods=['POST'])
def update_projects():
    return UpdateProject(request=request).update()

@project_Blueprint.route("/display-project",methods=['POST'])
def get_project():
    return DisplayProject(request=request).display()
    
@project_Blueprint.route("/list-project-users", methods=["POST"])
def list_project_users():
    return ListProjectUsers(request=request).list()

@project_Blueprint.route("/create-project-users", methods=["POST"])
def add_project_users():
    return CreateEmployeeUser(request=request).create()

@project_Blueprint.route("/send-invite", methods=["POST"])
def send_invite_to_employee():
    return SendInvite(request=request).send_invite()

@project_Blueprint.route("/project-employee-report", methods= ["GET"])
def project_employee_report():
    return EmployeeProjectReport().get_employee_project_report()

@project_Blueprint.route("/project-stages-report", methods= ["GET"])
def project_stages_report():
    return ProjectStagesReport().get_stage_employee_report(request)

@project_Blueprint.route("/project-user-delete", methods = ["POST"])
def project_employee_delete():
    return DeleteProjectUsers(request=request).delete()

@project_Blueprint.route("/project-task-overdue", methods = ["POST"])
def project_task_overdue():
    return ProjectTaskReportStatusHandler(request=request).projectOverdueTasks()

@project_Blueprint.route("/project-task-inprogress", methods = ["POST"])
def project_task_inprogress():
    return ProjectTaskReportStatusHandler(request=request).projectInProgressTasks()

@project_Blueprint.route("project-task-todo", methods = ["POST"])
def project_task_todo():
    return ProjectTaskReportStatusHandler(request=request).projectToDoTasks()



