from src.models import Employee, Task, Project , Stage
from src.database import db
from sqlalchemy import select, and_ , func
from flask import jsonify
from datetime import datetime

class ProjectTaskReportStatusHandler:
    def __init__(self, request) -> None:
        self.request = request
        self.session = db.session()

    def projectOverdueTasks(self):
        try:
            data = self.request.get_json()
            project_id = data.get("project_id")

            if not project_id:
                return jsonify({
                    "status": False,
                    "error": 1,
                    "data": [],
                    "message": "Missing required parameter: project_id"
                }), 400

            project_stmt = select(Project).where(Project.project_id == project_id)
            project = self.session.execute(project_stmt).scalar()

            if not project:
                return jsonify({
                    "status": False,
                    "error": 2,
                    "data": [],
                    "message": "Project not found"
                }), 404

            task_stmt = select(
                Task, Stage.name, Project.name, Employee.name  
            ).join(
                Stage, Task.stage_id == Stage.stage_id
            ).join(
                Project, Task.project_id == Project.project_id
            ).outerjoin(  
                Employee, Task.assignee_id == Employee.employee_id
            ).where(
                and_(
                    Task.project_id == project_id,
                    Task.status == "DONE", 
                    Task.actual_end_date.isnot(None),
                    Task.assignee_id.isnot(None),
                    Task.end_date.isnot(None),
                    Task.actual_end_date > Task.end_date
                )
            )

            result = self.session.execute(task_stmt).all()

            if not result:
                return jsonify({
                    "status": True,
                    "error": 0,
                    "project_name": project.name,  
                    "data": [],
                    "message": "No overdue tasks found"
                }), 200

            project_name = result[0][2] if result else project.name  

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
                "employee_name": employee_name if employee_name else "Unassigned",
            } for task, stage_name, _, employee_name in result]  

            return jsonify({
                "status": True,
                "error": 0,
                "project_name": project_name, 
                "data": response,
                "message": "Filtered overdue tasks retrieved successfully"
            }), 200

        except Exception as e:
            return jsonify({
                "status": False,
                "error": 5,
                "data": [],
                "message": f"Failed to fetch overdue tasks: {e}"
            }), 500

    
    def projectInProgressTasks(self):
        try:
            current_date = datetime.today().date()
            data = self.request.get_json()
            project_id = data.get("project_id")

            if not project_id:
                return jsonify({
                    "status": False,
                    "error": 1,
                    "data": [],
                    "message": "Missing required parameter: project_id"
                }), 400

            project_stmt = select(Project).where(Project.project_id == project_id)
            project = self.session.execute(project_stmt).scalar()

            if not project:
                return jsonify({
                    "status": False,
                    "error": 2,
                    "data": [],
                    "message": "Project not found"
                }), 404
            
            task_stmt = select(
                Task,
                Stage.name, 
                Project.name,
                Employee.name  
            ).outerjoin(
                Stage, Task.stage_id == Stage.stage_id
            ).outerjoin(
                Project, Task.project_id == Project.project_id
            ).outerjoin(  
                Employee, Task.assignee_id == Employee.employee_id
            ).where(
                and_(
                    Task.assignee_id.isnot(None),
                    Task.status == "IN_PROGRESS",
                    Task.end_date <= func.now()
                )
            )

            result = self.session.execute(task_stmt).all()

            if not result:
                return jsonify({
                    "status": True,
                    "error": 0,
                    "project_name": project.name,
                    "data": [],
                    "message": "No in-progress tasks found"
                }), 200

            project_name = result[0][2] if result else project.name

            response = []
            for task, stage_name, _, employee_name in result:
                extra_days = (
                    None if task.end_date is None 
                    else max(0, (current_date - task.end_date.date()).days)
                )

                if extra_days == 0:  
                    continue 

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
                    "employee_name": employee_name if employee_name else "Unassigned"
                })

            return jsonify({
                "status": True,
                "error": 0,
                "project_name": project_name,
                "data": response,
                "message": "Filtered in-progress tasks retrieved successfully"
            }), 200

        except Exception as e:
            return jsonify({
                "status": False,
                "error": 5,
                "data": [],
                "message": f"Failed to fetch in-progress tasks: {e}"
            }), 500
        
    def projectToDoTasks(self):
        try:
            current_date = datetime.today().date()
            data = self.request.get_json()
            project_id = data.get("project_id")

            if not project_id:
                return jsonify({
                    "status": False,
                    "error": 1,
                    "data": [],
                    "message": "Missing required parameter: project_id"
                }), 400

            project_stmt = select(Project).where(Project.project_id == project_id)
            project = self.session.execute(project_stmt).scalar()

            if not project:
                return jsonify({
                    "status": False,
                    "error": 2,
                    "data": [],
                    "message": "Project not found"
                }), 404

            task_stmt = select(
                Task,
                Stage.name, 
                Project.name,
                Employee.name  
            ).outerjoin(
                Stage, Task.stage_id == Stage.stage_id
            ).outerjoin(
                Project, Task.project_id == Project.project_id
            ).outerjoin(  
                Employee, Task.assignee_id == Employee.employee_id
            ).where(
                and_(
                    Task.assignee_id.isnot(None),
                    Task.status == "TODO",
                    Task.end_date.isnot(None)  
                )
            )

            result = self.session.execute(task_stmt).all()

            if not result:
                return jsonify({
                    "status": True,
                    "error": 0,
                    "project_name": project.name,
                    "data": [],
                    "message": "No TODO tasks found"
                }), 200

            project_name = result[0][2] if result else project.name

            response = []
            for task, stage_name, _, employee_name in result:
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
                    "employee_name": employee_name if employee_name else "Unassigned"
                })

            return jsonify({
                "status": True,
                "error": 0,
                "project_name": project_name,
                "data": response,
                "message": "Filtered TODO tasks retrieved successfully"
            }), 200

        except Exception as e:
            return jsonify({
                "status": False,
                "error": 5,
                "data": [],
                "message": f"Failed to fetch TODO tasks: {e}"
            }), 500
