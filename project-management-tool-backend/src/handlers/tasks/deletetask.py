from src.models.task import Task
from src.models.comments import Comments
from src.models.history import History  
from src.models.attachment import Attachment
from src.database import db
from sqlalchemy import delete, or_

class TaskDeleteHandler:

    def __init__(self):
        self.session = db.session()

    def delete(self, request):
        try:
            body = request.json
            task_id = body.get('task_id')
            delete_tasks = delete(Task).filter(Task.task_id == task_id)
            self.session.execute(delete_tasks)
            self.session.commit()
            return {
                "status": True,
                "error_code": 0,
                "message": "Task deleted successfully",
                "data": {}
            }

        except Exception as e:
            self.session.rollback()  # Roll back the transaction on error
            return {
                "status": False,
                "error": 1,
                "message": f"Task deletion unsuccessful due to {e}",
                "data": {}
            }
