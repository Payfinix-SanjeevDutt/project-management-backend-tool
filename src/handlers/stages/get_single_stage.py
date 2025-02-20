from flask import request
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.database import db
from src.models import Stage

class StageSingleHandler:
    def __init__(self):
        self.session = db.session()

    def get_single_stage(self, request):
        try:
            body = request.json
            stmt = select(Stage).where(Stage.stage_id == body["stage_id"])
            result = self.session.execute(stmt).scalar_one_or_none()
            if result:
                return {
                    "status": True,
                    "error": 0,
                    "data": {
                        "stage_id": result.stage_id,
                        "project_id": result.project_id,
                        "stage_name": result.name,
                        "description": result.description,
                        "start_date": result.start_date,
                        "actual_start_date": result.actual_start_date,
                        "end_date": result.end_date,
                        "actual_end_date": result.actual_end_date
                    }
                }
            else:
                return {
                    "status": False,
                    "error": 1,
                    "message": "Stage not found"
                }
        except Exception as e:
            return {
                "status": False,
                "error": 1,
                "message": f"Failed to retrieve stage due to {e}"
            }