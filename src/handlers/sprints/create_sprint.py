from src.database import db
from src.models import Sprint
from src.utils import generate_unique_key


class SprintCreateHandler:

    def __init__(self):
        self.session = db.session()

    def create(self, request):
        try:
            body = request.json

            sprint_object= Sprint(
                sprint_id=generate_unique_key(),
                project_id=body['project_id'],
                name=body['sprint_name'],
                description=body['description'],
                start_date=body['start_date'],
                created_by=body['created_by'],
                created_at=body['created_at'],
                actual_start_date=body['actual_start_date'],
                end_date=body['end_date'],
                actual_end_date=body['actual_end_date']
            )
            self.session.add(sprint_object)
            self.session.commit()
            return {
                "status": True,
                "error": 0,
                "message": "Stage created successfully",
                "data":{
                    "sprint_name" : sprint_object.name,
                    "sprint_id" : sprint_object.sprint_id
                }
            }
        except Exception as e:
            self.session.rollback() 
            return {
                "status": False,
                "error": 1,
                "message": f"Sprint creation unsuccessful due to {e}",
                "data" : {
                    "sprint_name" : ' ',
                    "sprint_id" : ' '
                }
            }

    
