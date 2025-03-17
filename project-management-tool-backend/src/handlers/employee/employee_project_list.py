from src.models import Employee, Task ,Stage,Project
from src.database import db
from sqlalchemy import select, and_, func
from flask import jsonify
from datetime import datetime

class EmployeeProjectTaskHandler:
    def __init__(self, request) -> None:
        self.request = request
        self.session = db.session()

    def employeeProjectTaskCompletedList(self):
        try:
            data = self.request.get_json()
            assignee_id = data.get("assignee_id")

            if not assignee_id:
                return jsonify({
                    "status": False,
                    "error": 1,
                    "data": [],
                    "message": "Missing required parameter: assignee_id"
                }), 400

            employee_stmt = select(Employee).where(Employee.employee_id == assignee_id)
            employee = self.session.execute(employee_stmt).scalar()

            if not employee:
                return jsonify({
                    "status": False,
                    "error": 2,
                    "data": [],
                    "message": "Employee not found"
                }), 404

            employee_name = employee.name

            task_stmt = select(
                            Task,
                            Stage.name,
                            Project.name
                        ).outerjoin(
                            Stage, Task.stage_id == Stage.stage_id
                        ).outerjoin(
                            Project, Task.project_id == Project.project_id
                        ).where(
                            and_(
                                Task.assignee_id == assignee_id,
                                Task.status == "DONE", 
                                Task.actual_end_date > Task.end_date 
                            )
                        )


            result = self.session.execute(task_stmt).all()

            response = [{
                "task_id": task.task_id,
                "task_name": task.task_name,
                "status": task.status,
                "start_date": task.start_date.strftime('%Y-%m-%d') if task.start_date else None,
                "end_date": task.end_date.strftime('%Y-%m-%d') if task.end_date else None,
                "actual_start_date": task.actual_start_date.strftime('%Y-%m-%d') if task.actual_start_date else None,
                "actual_end_date": task.actual_end_date.strftime('%Y-%m-%d') if task.actual_end_date else None,
                "assignee_id": task.assignee_id,
                "extra_days": (task.actual_end_date - task.end_date).days if task.actual_end_date and task.end_date else None,
                "stage_name": stage_name,
                "project_name": project_name
            } for task, stage_name, project_name in result]

            return jsonify({
                "status": True,
                "error": 0,
                "employee_name": employee_name,  
                "data": response,
                "message": "Filtered tasks retrieved successfully"
            }), 200

        except Exception as e:
            return jsonify({
                "status": False,
                "error": 5,
                "data": [],
                "message": f"Failed to fetch tasks: {e}"
            }), 500
        
    def employeeProjectTaskInprogressList(self):
        try:
            current_date = datetime.today().date()
            data = self.request.get_json()
            assignee_id = data.get("assignee_id")

            if not assignee_id:
                return jsonify({
                    "status": False,
                    "error": 1,
                    "data": [],
                    "message": "Missing required parameter: assignee_id"
                }), 400

            employee_stmt = select(Employee).where(Employee.employee_id == assignee_id)
            employee = self.session.execute(employee_stmt).scalar()

            if not employee:
                return jsonify({
                    "status": False,
                    "error": 2,
                    "data": [],
                    "message": "Employee not found"
                }), 404

            employee_name = employee.name

            task_stmt = select(
                Task,
                Stage.name,
                Project.name
            ).outerjoin(
                Stage, Task.stage_id == Stage.stage_id
            ).outerjoin(
                Project, Task.project_id == Project.project_id
            ).where(
                and_(
                    Task.assignee_id == assignee_id,
                    Task.status == "IN_PROGRESS",
                    Task.end_date.isnot(None),
                    Task.end_date <= func.now()
                )
            )
            
            result = self.session.execute(task_stmt).all()

            response = []
            for task, stage_name, project_name in result:
                extra_days = (
                    (current_date - task.end_date.date()).days
                    if task.end_date and current_date >= task.end_date.date() 
                    else None
                )

                if extra_days == 0:  
                    continue  # Skip task if no extra days

                response.append({
                    "task_id": task.task_id,
                    "task_name": task.task_name,
                    "status": task.status,
                    "start_date": task.start_date.strftime('%Y-%m-%d') if task.start_date else None,
                    "end_date": task.end_date.strftime('%Y-%m-%d') if task.end_date else None,
                    "actual_start_date": task.actual_start_date.strftime('%Y-%m-%d') if task.actual_start_date else None,
                    "actual_end_date": task.actual_end_date.strftime('%Y-%m-%d') if task.actual_end_date else None,
                    "assignee_id": task.assignee_id,
                    "extra_days": extra_days,  
                    "stage_name": stage_name,
                    "project_name": project_name
                })

            return jsonify({
                "status": True,
                "error": 0,
                "employee_name": employee_name,  
                "data": response,
                "message": "Filtered tasks retrieved successfully"
            }), 200

        except Exception as e:
            return jsonify({
                "status": False,
                "error": 5,
                "data": [],
                "message": f"Failed to fetch tasks: {e}"
            }), 500



    def employeeProjectTaskToDoList(self):
        try:
            current_date = datetime.today().date()
            data = self.request.get_json()
            assignee_id = data.get("assignee_id")

            if not assignee_id:
                return jsonify({
                    "status": False,
                    "error": 1,
                    "data": [],
                    "message": "Missing required parameter: assignee_id"
                }), 400

            employee_stmt = select(Employee).where(Employee.employee_id == assignee_id)
            employee = self.session.execute(employee_stmt).scalar()

            if not employee:
                return jsonify({
                    "status": False,
                    "error": 2,
                    "data": [],
                    "message": "Employee not found"
                }), 404

            employee_name = employee.name

            task_stmt = select(
                Task, Stage.name, Project.name
            ).join(
                Stage, Task.stage_id == Stage.stage_id
            ).join(
                Project, Stage.project_id == Project.project_id
            ).where(
                and_(
                    Task.assignee_id == assignee_id,
                    Task.status == "TODO",
                    Task.end_date.isnot(None)  
                )
            )

            result = self.session.execute(task_stmt).all()

            response = []
            for task, stage_name, project_name in result:
                extra_days = (
                    (current_date - task.end_date.date()).days
                    if task.end_date and current_date >= task.end_date.date() 
                    else None
                )

                if extra_days == 0:  
                    continue  

                response.append({
                    "task_id": task.task_id,
                    "task_name": task.task_name,
                    "status": task.status,
                    "start_date": task.start_date.strftime('%Y-%m-%d') if task.start_date else None,
                    "end_date": task.end_date.strftime('%Y-%m-%d') if task.end_date else None,
                    "assignee_id": task.assignee_id,
                    "extra_days": extra_days,  
                    "stage_name": stage_name,
                    "project_name": project_name
                })

            return jsonify({
                "status": True,
                "error": 0,
                "employee_name": employee_name,  
                "data": response,
                "message": "Filtered TO-DO tasks retrieved successfully"
            }), 200

        except Exception as e:
            return jsonify({
                "status": False,
                "error": 5,
                "data": [],
                "message": f"Failed to fetch tasks: {e}"
            }), 500


