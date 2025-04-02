from sqlalchemy import func, case, Date
from sqlalchemy.sql import distinct, and_, or_
from datetime import date
from src.database import db
from src.models import Employee, Task, TaskStatus, Project, Stage, ProjectUsers


class ProjectStagesReport:
    def __init__(self):
        self.session = db.session

    def get_stage_employee_report(self, request):
        try:
            project_query = db.session.query(
                Project.project_id,
                Project.name.label("project_name"),
                func.count(distinct(Stage.stage_id)).label("total_stages"),
                func.count(distinct(ProjectUsers.employee_id)
                           ).label("number_employees")
            ).outerjoin(Stage, Project.project_id == Stage.project_id) \
                .outerjoin(ProjectUsers, Project.project_id == ProjectUsers.project_id) \
                .group_by(Project.project_id).all()

            if not project_query:
                return {"message": "No projects found"}, 404

            projects_summary = []

            for project in project_query:
                task_summary = (
                    db.session.query(
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
                        ).label("delayed_tasks"),
                        func.sum(
                            case(
                                (and_(Task.status == TaskStatus.DONE,Task.assignee_id.isnot(None),
                                 Task.actual_end_date > Task.end_date), 1),
                                else_=0,
                            )
                        ).label("completed_overrun"),
                        func.sum(
                            case(
                                (and_(Task.status == TaskStatus.IN_PROGRESS, Task.assignee_id.isnot(None),
                                 func.current_date() > Task.end_date), 1),
                                else_=0,
                            )
                        ).label("inprogress_overrun"),
                    )
                    .join(Stage, Stage.stage_id == Task.stage_id)
                    .filter(Stage.project_id == project.project_id)
                    .first()
                )

                projects_summary.append({
                    "project_id": project.project_id,
                    "project_name": project.project_name,
                    "total_stages": project.total_stages or 0,
                    "number_employees": project.number_employees or 0,
                    "total_tasks": task_summary.total_tasks or 0,
                    "completed_tasks": task_summary.completed_tasks or 0,
                    "inprogress_tasks": task_summary.inprogress_tasks or 0,
                    "delayed_tasks": task_summary.delayed_tasks or 0,
                    "completed_overrun": task_summary.completed_overrun or 0,
                    "inprogress_overrun": task_summary.inprogress_overrun or 0,
                })

            return {"projects": projects_summary}

        except Exception as e:
            return {"message": f"Error: {e}"}, 500
