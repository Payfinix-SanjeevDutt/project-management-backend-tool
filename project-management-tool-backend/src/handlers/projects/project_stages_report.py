from sqlalchemy import func, case, Date
from sqlalchemy.sql import distinct, and_
from datetime import date
from src.database import db
from src.models import Employee, Task, TaskStatus, Project, Stage

class ProjectStagesReport:
    def __init__(self):
        self.session = db.session

    def get_stage_employee_report(self, request):
        try:
            body = request.get_json()
            project_ids = body.get("project_id", [])

            if not project_ids:
                return {"message": "project_id is required"}, 400

            # Fetch project details along with stage count
            project_data = (
                db.session.query(
                    Project.project_id,
                    Project.name.label("project_name"),
                    func.count(Stage.stage_id).label("total_stages")
                )
                .outerjoin(Stage, Project.project_id == Stage.project_id)
                .filter(Project.project_id.in_(project_ids))
                .group_by(Project.project_id)
                .all()
            )

            if not project_data:
                return {"message": "Projects not found"}, 404

            # Collect all project-wise data
            projects_summary = []

            for project in project_data:
                # Aggregate task summary for each project
                task_summary = (
                    db.session.query(
                        func.count(Task.task_id).label("total_tasks"),
                        func.sum(case((Task.status == TaskStatus.DONE, 1), else_=0)).label("completed_tasks"),
                        func.sum(case((Task.status == TaskStatus.IN_PROGRESS, 1), else_=0)).label("inprogress_tasks"),
                        func.sum(case((Task.status == TaskStatus.TODO, 1), else_=0)).label("pending_tasks"),
                        func.sum(
                            case(
                                (and_(Task.status == TaskStatus.DONE, Task.actual_end_date > Task.end_date), 1),
                                else_=0,
                            )
                        ).label("completed_overrun"),
                        func.sum(
                            case(
                                (and_(Task.status == TaskStatus.IN_PROGRESS, func.current_date() > Task.end_date), 1),
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
                    "total_tasks": task_summary.total_tasks or 0,
                    "completed_tasks": task_summary.completed_tasks or 0,
                    "inprogress_tasks": task_summary.inprogress_tasks or 0,
                    "pending_tasks": task_summary.pending_tasks or 0,
                    "completed_overrun": task_summary.completed_overrun or 0,
                    "inprogress_overrun": task_summary.inprogress_overrun or 0,
                })

            return {"projects": projects_summary}

        except Exception as e:
            return {"message": f"Error: {e}"}, 500

