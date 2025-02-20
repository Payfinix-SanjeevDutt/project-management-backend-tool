from sqlalchemy import delete
from src.database import db
from src.models import Stage, Task , Attachment,Comments,History

class StageDeleteHandler:
    def __init__(self):
        self.session = db.session()

    def delete_stage(self, request):
        try:
            body = request.json
            stage_id = body['stage_id']
            
            delete_stage_stmt = delete(Stage).where(Stage.stage_id == stage_id)
            self.session.execute(delete_stage_stmt)
            self.session.commit()

            return {
                "status": True,
                "error": 0,
                "message": "Stage and associated tasks deleted successfully"
            }

        except Exception as e:
            self.session.rollback()
            return {
                "status": False,
                "error": 1,
                "message": f"Stage deletion unsuccessful due to {e}"
            }
