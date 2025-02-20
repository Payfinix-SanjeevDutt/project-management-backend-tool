from src.database import db
from src.models import Sprint, Task, Employee
from sqlalchemy.orm import aliased
from sqlalchemy import select


class SprintListHandler:
   
   def __init__(self):
        self.session = db.session()

   def list_sprint(self, request):
    try:
        body = request.json

        # Fetch all sprints for the given project ID
        all_sprints = Sprint.query.filter_by(project_id=body['project_id']).all()
        print("Sprint list:", all_sprints)

        sprints = []
        for sprint in all_sprints:
            # Aliasing Employee model for reporter and assignee
            reporter_alias = aliased(Employee, name="reporter")
            assignee_alias = aliased(Employee, name="assignee")

            # Query to fetch tasks for the current sprint, along with reporter and assignee details
            query = (
                select(
                    Task,
                    reporter_alias.name.label("rname"),
                    reporter_alias.avatar.label("ravatar"),
                    reporter_alias.email.label("remail"),
                    assignee_alias.name.label("aname"),
                    assignee_alias.avatar.label("aavatar"),
                    assignee_alias.email.label("aemail")
                )
                .select_from(Task)
                .outerjoin(reporter_alias, Task.reporter_id == reporter_alias.employee_id)
                .outerjoin(assignee_alias, Task.assignee_id == assignee_alias.employee_id)
                .filter(Task.sprint_id == sprint.sprint_id)  # Filter by sprint_id
            )

            # Execute the query and fetch all results
            result = self.session.execute(query).all()

            # Format tasks as a list of dictionaries
            task_list = [
                {
                    "task_id": task.task_id,
                    "task_name": task.task_name,
                    "description": task.description,
                    "status": task.status,
                    "priority": task.priority,
                    "start_date": task.start_date,
                    "end_date": task.end_date,
                    "sprint_id": task.sprint_id,
                    "assignee_id": task.assignee_id,
                    "reporter_id": task.reporter_id,
                    "reporter_name": rname,
                    "reporter_avatar": ravatar,
                    "reporter_email": remail,
                    "assignee_name": aname,
                    "assignee_avatar": aavatar,
                    "assignee_email": aemail,
                    "children": [] 
                }
                for task, rname, ravatar, remail, aname, aavatar, aemail in result
            ] if result else None

            # Add sprint details with associated tasks
            sprints.append({
                "sprint_id": sprint.sprint_id,
                "project_id": sprint.project_id,
                "sprint_name": sprint.name,
                "description": sprint.description,
                "start_date": sprint.start_date,
                "actual_start_date": sprint.actual_start_date,
                "end_date": sprint.end_date,
                "actual_end_date": sprint.actual_end_date,
                "tasks": task_list  # Include tasks or None if no tasks
            })

        return {
            "status": True,
            "error": 0,
            "data": sprints
        }
    except Exception as e:
        return {
            "status": False,
            "error": 1,
            "message": f"Failed to retrieve sprints due to {e}"
        }

