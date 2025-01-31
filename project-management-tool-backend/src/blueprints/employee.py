from flask import Blueprint, request

from src.handlers import EmployeeHandler, UpdateEmployee, DeleteEmployee, SecurityEmpoyee

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


