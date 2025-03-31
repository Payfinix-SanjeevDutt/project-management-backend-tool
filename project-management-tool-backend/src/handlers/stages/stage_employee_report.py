from flask import request
from sqlalchemy import func, case
from sqlalchemy.sql import distinct, and_ ,or_
from src.database import db
from src.models import Task, TaskStatus, Stage

class EmployeeStageReport:
    def __init__(self):
        self.session = db.session

    def get_stage_employee_report(self, request):
        try:
            body = request.get_json()
            project_id = body.get("project_id")

            if not project_id:
                return {"message": "project_id is required"}, 400

            unique_employees = (
                db.session.query(Stage.stage_id.label("stage_id"), Task.assignee_id.label("employee_id"))
                .filter(Stage.project_id == project_id, Task.assignee_id != None)
                .join(Task, Stage.stage_id == Task.stage_id)
                .union_all(
                    db.session.query(Stage.stage_id.label("stage_id"), Task.reporter_id.label("employee_id"))
                    .filter(Stage.project_id == project_id, Task.reporter_id != None)
                    .join(Task, Stage.stage_id == Task.stage_id)
                )
                .subquery()
            )

            unique_employee_count = (
                db.session.query(
                    unique_employees.c.stage_id,
                    func.count(distinct(unique_employees.c.employee_id)).label("num_unique_employees")
                )
                .group_by(unique_employees.c.stage_id)
                .subquery()
            )

            stage_report = (
                db.session.query(
                    Stage.stage_id,
                    Stage.name,
                    func.count(
                            case(
                               ((Task.assignee_id.isnot(None)), Task.task_id),
                                else_=None
                            )
                        ).label("total_tasks"),

                        func.sum(case((and_(Task.status == TaskStatus.DONE, Task.assignee_id.isnot(None)), 1), else_=0)).label(
                            "completed_tasks"),
                        func.sum(case((and_(Task.status == TaskStatus.IN_PROGRESS, Task.assignee_id.isnot(None)), 1), else_=0)).label(
                            "inprogress_tasks"),
                        func.sum(
                            case(
                                (
                                    and_(
                                        Task.status == TaskStatus.TODO,
                                        Task.assignee_id.isnot(None)
                                    ), 1 
                                ),
                                else_=0,
                            )
                        ).label("pending_tasks"),
                    func.sum(
                        case(
                            (and_(Task.status == TaskStatus.DONE,  Task.assignee_id.isnot(None),Task.actual_end_date > Task.end_date), 1),
                            else_=0,
                        )
                    ).label("completed_overrun"),
                    func.sum(
                        case(
                            (and_(Task.status == TaskStatus.IN_PROGRESS, Task.assignee_id.isnot(None), func.current_date() > Task.end_date), 1),
                            else_=0,
                        )
                    ).label("inprogress_overrun"),
                    func.coalesce(unique_employee_count.c.num_unique_employees, 0).label("num_unique_employees")
                )
                .filter(Stage.project_id == project_id)
                .outerjoin(Task, Stage.stage_id == Task.stage_id)
                .outerjoin(unique_employee_count, unique_employee_count.c.stage_id == Stage.stage_id) 
                .group_by(Stage.stage_id, Stage.name, unique_employee_count.c.num_unique_employees)
                .order_by(Stage.name)
            ).all()

            return [
                {
                    "stage_id":row.stage_id,
                    "stage_name": row.name,
                    "num_unique_employees": row.num_unique_employees or 0, 
                    "total_tasks": row.total_tasks or 0,
                    "completed_tasks": row.completed_tasks or 0,
                    "inprogress_tasks": row.inprogress_tasks or 0,
                    "pending_tasks": row.pending_tasks or 0,
                    "completed_overrun": row.completed_overrun or 0,
                    "inprogress_overrun": row.inprogress_overrun or 0,
                }
                for row in stage_report
            ]

        except Exception as e:
            return {"message": f"Error: {e}"}, 500
