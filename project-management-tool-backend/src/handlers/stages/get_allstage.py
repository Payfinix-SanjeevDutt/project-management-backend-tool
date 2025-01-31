from flask import request
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.database import db
from src.models import Stage


class AllStageHandler:
    def __init__(self):
        self.session = db.session()


    def get_all_stage(self,request):
        try:
            body  = request.json
            stmt = select(Stage).where(Stage.project_id == body['project_id'])
            result = self.session.execute(stmt).scalars().all()
            stages = []
            for stage in result:
                stages.append({
                    "stage_id": stage.stage_id,
                    "project_id": stage.project_id,
                    "stage_name": stage.name,
                    "description": stage.description,
                    "start_date": stage.start_date,
                    "actual_start_date": stage.actual_start_date,
                    "end_date": stage.end_date,
                    "actual_end_date": stage.actual_end_date
                })
            return {
                "status": True,
                "error": 0,
                "data": stages
            }
        except Exception as e:
            return {
                "status": False,
                "error": 1,
                "message": f"Failed to retrieve stages due to {e}"
            }