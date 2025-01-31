from sqlalchemy import func, case, Date
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import and_
from datetime import date
from src.database import db
from src.models import Employee, Task, TaskStatus, Project, Stage

class EmployeeTaskReport:
    def __init__(self):
        self.session = db.session

    def get_employee_task_report(self, request):
        try:
            body = request.get_json()
            project_id = body.get('project_id')  
            
            if not project_id:
                return {"message": "project_id is required"}, 400
            
            task_counts = (
                db.session.query(
                    Employee.employee_id,
                    Employee.name,
                    Employee.email,
                    Employee.avatar,
                    Project.project_id,
                    func.count(Task.task_id).label('total_tasks'),
                    func.sum(case((Task.status == TaskStatus.DONE, 1), else_=0)).label('completed_tasks'),
                    func.sum(case((Task.status == TaskStatus.IN_PROGRESS, 1), else_=0)).label('inprogress_tasks'),
                    func.sum(case((Task.status == TaskStatus.TODO, 1), else_=0)).label('pending_tasks'),
                    func.sum(case((Task.parent_id != None, 1), else_=0)).label('total_subtasks'), 
                    func.sum(
                        case(
                            (and_(Task.status == TaskStatus.DONE, Task.actual_end_date > Task.end_date), 1),
                            else_=0,
                        )
                    ).label('completed_overrun'),
                    func.sum(
                        case(
                            (and_(Task.status == TaskStatus.IN_PROGRESS, func.current_date() > Task.end_date), 1),
                            else_=0,
                        )
                    ).label('inprogress_overrun')
                )
                .outerjoin(Task, Employee.employee_id == Task.assignee_id)
                .outerjoin(Stage, Stage.stage_id == Task.stage_id)  
                .outerjoin(Project, Project.project_id == Stage.project_id)  
                .filter(Project.project_id == project_id)  
                .group_by(Employee.employee_id, Project.project_id)
                .order_by(Employee.name)
            ).all()

            report = [
                {
                    "employee_id": emp.employee_id,
                    "name": emp.name,
                    "email": emp.email,
                    "avatar":emp.avatar,
                    "project_id": emp.project_id,
                    "total_tasks": emp.total_tasks,
                    "total_subtasks": emp.total_subtasks,
                    "main_tasks": emp.total_tasks - emp.total_subtasks,
                    "completed_tasks": emp.completed_tasks,
                    "inprogress_tasks": emp.inprogress_tasks,
                    "pending_tasks": emp.pending_tasks,
                    "completed_overrun": emp.completed_overrun,
                    "inprogress_overrun": emp.inprogress_overrun,
                }
                for emp in task_counts
            ]

            return report
        
        except Exception as e:
            return {
                "message": f"mistake {e}"
            }
