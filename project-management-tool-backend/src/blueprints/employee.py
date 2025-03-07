from flask import Blueprint, request

from src.handlers import EmployeeHandler, UpdateEmployee, DeleteEmployee, SecurityEmpoyee , EmployeeProjectTaskHandler

employee_blueprint = Blueprint("employee",__name__)

@employee_blueprint.route("/",methods=["GET"])
def getEmployees():
    return EmployeeHandler(request=request).getemployees()

@employee_blueprint.route("/update",methods=['POST'])
def updateEmployee():
    return UpdateEmployee(request=request).update()

@employee_blueprint.route("/delete",methods=["DELETE"])
def deleteEmployee():
    return DeleteEmployee(request=request).delete()

@employee_blueprint.route("/security", methods=['POST'])
def secureEmployee():
    return SecurityEmpoyee(request=request).security()

@employee_blueprint.route("/completed-overrun", methods=['POST'])
def EmployeeProjectTask():
    return EmployeeProjectTaskHandler(request=request).employeeProjectTaskCompletedList()

@employee_blueprint.route("/inprogress-overrun", methods=['POST'])
def EmployeeProjectTask2():
    return EmployeeProjectTaskHandler(request=request).employeeProjectTaskInprogressList()

@employee_blueprint.route("/todo", methods=['POST'])
def EmployeeProjectTask3():
    return EmployeeProjectTaskHandler(request=request).employeeProjectTaskToDoList()


