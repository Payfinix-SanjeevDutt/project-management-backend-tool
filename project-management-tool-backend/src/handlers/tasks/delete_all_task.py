from src.models.task import Task
from src.models.comments import Comments
from src.models.history import History
from src.database import db
from sqlalchemy import delete, or_

class AllTaskDeleteHandler:

    def __init__(self):
        self.session = db.session()

    def delete_all(self, request):
        try:
            body = request.json
            task_ids = body.get("task_ids", [])
                        
            tasks = delete(Task).filter(Task.task_id.in_(task_ids))
            self.session.execute(tasks)
            self.session.commit()
         
            return {
                "status": True,
                "error_code": 0,
                "message": f"Tasks deleted successfully",
                "data": {}
            }

        except Exception as e:
            return {
                "status": False,
                "error_code": 1,
                "message": f"Task deletion unsuccessful due to {e}",
                "data": {}
            }
