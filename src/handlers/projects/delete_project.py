from src.database import db
from src.models import Project, ProjectUsers, Stage, Task
from sqlalchemy import delete
from src.services.sharepoint.file_manager.actions import SharepointFileManager
from flask import jsonify


class DeleteProject:
    def __init__(self, request):
        self.request = request
        self.db = db.session()

    def delete(self):
        try:
            body = self.request.json
            project_id = body.get('project_id')

            folder_path_parts = ["Projects", project_id] 
            folder_path = "/".join(folder_path_parts)
            print("Constructed folder path:", folder_path)

            sharepoint_manager = SharepointFileManager(requestData=body)
            folder_delete_response = sharepoint_manager.delete_folder(folder_path)
            print("folder delete", folder_delete_response)

            query = delete(Project).where(Project.project_id==project_id)
            self.db.execute(query)
            self.db.commit()

 
            return jsonify({
                "status": True,
                "error_code": 0,
                "message": "Project deleted successfully"
            }), 200

        except Exception as e:
            print(e)
            return jsonify({
                "status": False,
                "error_code": 2,
                "message": f"Failed to delete project: {e}"
            }), 500
