from flask import request
from sqlalchemy import delete
from src.database import db
from src.models import Sprint


class SprintDeleteHandler:
    def __init__(self):
        self.session = db.session()

    def delete_sprint(self,request):
        try:
            body = request.json
            stmt = delete(Sprint).where(Sprint.sprint_id == body['sprint_id'])
            result = self.session.execute(stmt)
            if result.rowcount == 0:  
                return {
                    "status": False,
                    "error": 1,
                    "message": "Sprint not found"
                }
            self.session.commit()
            return {
                "status": True,
                "error": 0,
                "message": "Sprint deleted successfully"
            }
        except Exception as e:
            self.session.rollback() 
            return {
                "status": False,
                "error": 1,
                "message": f"Sprint deletion unsuccessful due to {e}"
            }

