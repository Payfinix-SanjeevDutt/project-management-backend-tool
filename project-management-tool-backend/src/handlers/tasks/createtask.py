from src.models.task import Task
from src.database import db
from src.utils import generate_unique_key

class TaskCreateHandler:

    def __init__(self):
        self.session = db.session()

    def create(self, request):
        try:
            body = request.json
            task_object = Task(
                task_id=generate_unique_key(),  
                task_name = body.get('task_name',None),
                stage_id = body.get('stage_id',None),
                sprint_id = body.get('sprint_id',None),
                project_id = body['project_id'],
                parent_id = body.get('parent_id',None)
            )
            self.session.add(task_object)
            self.session.commit()
            return {
                "status": True,
                "error_code": 0,
                "message": "Task created successfully",
                "data": {
                    **task_object.get_details(),
                    "reporter_email": None,
                    "reporter_name": None,
                    "reporter_id": None,
                    "reporter_avatar": None,
                    "actual_end_date": None,
                    "actual_start_date": None,
                    "assignee_avatar": None,
                    "assignee_email": None,
                    "assignee_name": None,
                    "assignee_id": None,
                    "childern":[],
                }
            }
        except Exception as e:
            return {
                "status": False,
                "error_code": 1,
                "message": f"Task creation unsuccessful due to {e}",
                "data": {}
            }