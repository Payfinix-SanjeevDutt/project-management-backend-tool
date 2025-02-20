from src.database import db
from src.models import Stage
from src.utils import generate_unique_key
from src.services.sharepoint.file_manager.actions import SharepointFileManager


class StageCreateHandler:

    def __init__(self):
        self.session = db.session()

    def create(self, request):
        try:
            body = request.json

            stage_id=generate_unique_key()
            project_id=body['project_id']
            stage_object = Stage(
                stage_id=stage_id,
                project_id=project_id,
                name=body['stage_name'],
                description=body['description'],
                start_date=body['start_date'],
                actual_start_date=body.get('actual_start_date',None),
                end_date=body['end_date'],
                actual_end_date=body.get('actual_end_date',None)
            )
            requestData = {
                "folder_name": stage_id,
                "path": f"Projects/{project_id}/"
            }

            stage_folder = SharepointFileManager(requestData).createFolder()
            print("stage_folder", stage_folder)

            self.session.add(stage_object)
            self.session.commit()
            return {
                "status": True,
                "error": 0,
                "message": "Stage created successfully",
                "data": {
                    "stage_name": stage_object.name,
                    "stage_id": stage_object.stage_id
                }
            }
        except Exception as e:
            self.session.rollback()
            return {
                "status": False,
                "error": 1,
                "message": f"Stage creation unsuccessful due to {e}",
                "data": {
                    "stage_name": ' ',
                    "stage_id": ' '
                }
            }
