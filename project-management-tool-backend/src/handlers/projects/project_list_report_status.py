from src.models import Employee, Task, Project
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

            task_stmt = select(Task).where(
                and_(
                    Task.project_id == project_id,
                    Task.status == "DONE", 
                    Task.actual_end_date > Task.end_date
                )
            )

            result = self.session.execute(task_stmt).scalars().all()

            response = [{
                "task_id": task.task_id,
                "task_name": task.task_name,
                "status": task.status,
                "start_date": task.start_date.strftime('%Y-%m-%d') if task.start_date else None,
                "end_date": task.end_date.strftime('%Y-%m-%d') if task.end_date else None,
                "actual_start_date": task.actual_start_date.strftime('%Y-%m-%d') if task.actual_start_date else None,
                "actual_end_date": task.actual_end_date.strftime('%Y-%m-%d') if task.actual_end_date else None,
                "assignee_id": task.assignee_id,
            } for task in result]

            return jsonify({
                "status": True,
                "error": 0,
                "project_name": project.name,
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

            task_stmt = select(Task).where(
                and_(
                    Task.project_id == project_id,
                    Task.status == "IN_PROGRESS", 
                    func.now() > Task.end_date
                )
            )

            result = self.session.execute(task_stmt).scalars().all()

            response = [{
                "task_id": task.task_id,
                "task_name": task.task_name,
                "status": task.status,
                "start_date": task.start_date.strftime('%Y-%m-%d') if task.start_date else None,
                "end_date": task.end_date.strftime('%Y-%m-%d') if task.end_date else None,
                "actual_start_date": task.actual_start_date.strftime('%Y-%m-%d') if task.actual_start_date else None,
                "actual_end_date": task.actual_end_date.strftime('%Y-%m-%d') if task.actual_end_date else None,
                "assignee_id": task.assignee_id,
            } for task in result]

            return jsonify({
                "status": True,
                "error": 0,
                "project_name": project.name,
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