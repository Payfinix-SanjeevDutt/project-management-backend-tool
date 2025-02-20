from flask import request
from sqlalchemy import update
from sqlalchemy.orm import Session
from src.database import db
from src.models import Stage

class StageUpdateHandler:
    def __init__(self):
        self.session: Session = db.session()

    def stage_update(self, request):
        try:
            body = request.json
            
            existing_stage = self.session.query(Stage).filter(Stage.stage_id == body['stage_id']).first()
            if not existing_stage:
                return {
                    "status": False,
                    "error": 1,
                    "message": "Stage ID not found"
                }

            stmt = (
                update(Stage)
                .where(Stage.stage_id == body['stage_id'])
                .values(**body)
            )

            self.session.execute(stmt)
            self.session.commit()
            return {
                "status": True,
                "error": 0,
                "message": "Stage updated successfully"
            }
        except Exception as e:
            return {
                "status": False,
                "error": 1,
                "message": f"Stage update unsuccessful due to {e}"
            }
