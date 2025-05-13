from sqlalchemy import func, case, and_
from datetime import date
from src.database import db
from src.models import Employee, Task, TaskStatus, Project, Stage


class EmployeeProjectReport:
    def __init__(self):
        self.session = db.session
 
    def get_employee_project_report(self):
        try:
            task_counts = (
                db.session.query(
                    Employee.employee_id,
                    Employee.name,
                    Employee.email,
                    Employee.avatar,
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
                    ).label('inprogress_overrun'),
                    func.count(func.distinct(Project.project_id)).label('total_projects'),
                    func.max(Task.end_date).label("latest_task_end_date")  # <-- added to calculate availability
                )
                .outerjoin(Task, Employee.employee_id == Task.assignee_id)
                .outerjoin(Stage, Stage.stage_id == Task.stage_id)
                .outerjoin(Project, Project.project_id == Stage.project_id)
                .group_by(Employee.employee_id)
                .order_by(Employee.name)
            ).all()

            report = []
            today = date.today()

            for emp in task_counts:
                if emp.latest_task_end_date:
                    latest_date = emp.latest_task_end_date.date()  # convert datetime to date
                    days_until_available = (latest_date - today).days
                    available_in = f"{days_until_available} day(s)" if days_until_available > 0 else "Available"
                else:
                    available_in = "Available"


                report.append({
                    "employee_id": emp.employee_id,
                    "name": emp.name,
                    "email": emp.email,
                    "avatar": emp.avatar,
                    "total_tasks": emp.total_tasks,
                    "total_subtasks": emp.total_subtasks,
                    "main_tasks": emp.total_tasks - emp.total_subtasks,
                    "completed_tasks": emp.completed_tasks,
                    "inprogress_tasks": emp.inprogress_tasks,
                    "pending_tasks": emp.pending_tasks,
                    "completed_overrun": emp.completed_overrun,
                    "inprogress_overrun": emp.inprogress_overrun,
                    "total_projects": emp.total_projects,
                    "available_in": available_in  # <-- include this in response
                })
            return report
 
        except Exception as e:
            return {
                "message": f"mistake {e}"
            }




# from sqlalchemy import func, case, Date
# from sqlalchemy.sql import distinct, and_
# from datetime import date
# from src.database import db
# from src.models import Employee, Task, TaskStatus, Project, Stage

# class EmployeeProjectReport:
#     def __init__(self):
#         self.session = db.session

#     def get_employee_project_report(self):
#         try:
#             task_counts = (
#                 db.session.query(
#                     Employee.employee_id,
#                     Employee.name,
#                     Employee.email,
#                     Employee.avatar,
#                     func.count(Task.task_id).label('total_tasks'),
#                     func.sum(case((Task.status == TaskStatus.DONE, 1), else_=0)).label('completed_tasks'),
#                     func.sum(case((Task.status == TaskStatus.IN_PROGRESS, 1), else_=0)).label('inprogress_tasks'),
#                     func.sum(case((Task.status == TaskStatus.TODO, 1), else_=0)).label('pending_tasks'),
#                     func.sum(case((Task.parent_id != None, 1), else_=0)).label('total_subtasks'),
#                     func.sum(
#                         case(
#                             (and_(Task.status == TaskStatus.DONE, Task.actual_end_date > Task.end_date), 1),
#                             else_=0,
#                         )
#                     ).label('completed_overrun'),
#                     func.sum(
#                         case(
#                             (and_(Task.status == TaskStatus.IN_PROGRESS, func.current_date() > Task.end_date), 1),
#                             else_=0,
#                         )
#                     ).label('inprogress_overrun'),
#                     func.count(func.distinct(Project.project_id)).label('total_projects')  
#                 )
#                 .outerjoin(Task, Employee.employee_id == Task.assignee_id)
#                 .outerjoin(Stage, Stage.stage_id == Task.stage_id)
#                 .outerjoin(Project, Project.project_id == Stage.project_id)
#                 .group_by(Employee.employee_id) 
#                 .order_by(Employee.name)
#             ).all()

#             report = [
#                 {
#                     "employee_id": emp.employee_id,
#                     "name": emp.name,
#                     "email": emp.email,
#                     "avatar": emp.avatar,
#                     "total_tasks": emp.total_tasks,
#                     "total_subtasks": emp.total_subtasks,
#                     "main_tasks": emp.total_tasks - emp.total_subtasks,
#                     "completed_tasks": emp.completed_tasks,
#                     "inprogress_tasks": emp.inprogress_tasks,
#                     "pending_tasks": emp.pending_tasks,
#                     "completed_overrun": emp.completed_overrun,
#                     "inprogress_overrun": emp.inprogress_overrun,
#                     "total_projects": emp.total_projects, 
#                 }
#                 for emp in task_counts
#             ]

#             return report

#         except Exception as e:
#             return {
#                 "message": f"mistake {e}"
#             }
