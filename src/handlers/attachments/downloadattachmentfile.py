from src.models.task import Task
from flask import request
from src.database import db
from src.services.sharepoint.file_manager.actions import SharepointFileManager
from src.database import db
from src.models import Attachment

class AttachmentDownloadHandler:

    def __init__(self, request):
        self.session = db.session()
        self.request = request

    def downloadattachment(self):
        try:
            # Parse input data
            data = request.get_json()
            # data = dataset['payload']
            print("data",data)
            project_id = data.get("project_id")
            stage_id = data.get("stage_id")
            task_id = data.get("task_id")
            subtask_id = data.get("subtask_id")
            file_name = data.get("file_name")

            if not file_name:
                return {
                    "status": False,
                    "error": 1,
                    "message": "File name is required.",
                    "data": {}
                }

            # Query to determine hierarchy
            if subtask_id:
                attachment = self.session.query(Attachment).filter(Attachment.subtask_id == subtask_id).first()
            elif task_id:
                attachment = self.session.query(Attachment).filter(Attachment.task_id == task_id).first()
            elif stage_id:
                attachment = self.session.query(Attachment).filter(Attachment.stage_id == stage_id).first()
            elif project_id:
                attachment = self.session.query(Attachment).filter(Attachment.project_id == project_id).first()
            else:
                return {
                    "status": False,
                    "error": 1,
                    "message": "At least one of project_id, stage_id, task_id, or subtask_id must be provided.",
                    "data": {}
                }

            if not attachment:
                return {
                    "status": False,
                    "error": 1,
                    "message": "No attachment found for the provided identifiers.",
                    "data": {}
                }

            # Build the folder path dynamically
            folder_path_parts = ["Projects"]
            if attachment.project_id:
                folder_path_parts.append(str(attachment.project_id))
            if attachment.stage_id:
                folder_path_parts.append(str(attachment.stage_id))
            if attachment.task_id:
                folder_path_parts.append(str(attachment.task_id))
            if attachment.subtask_id:
                folder_path_parts.append(str(attachment.subtask_id))
            folder_path_parts.append(file_name)

            file_path = "/".join(folder_path_parts)
            print("Constructed file path:", file_path)

            # Initialize SharepointFileManager with requestData
            sharepoint_manager = SharepointFileManager(requestData=data)
            folder_files_response = sharepoint_manager.download_file(file_path)
            return  {
                "status": True,
                "message": f"File download successful",
                "download_url": folder_files_response
            }
        

        except Exception as e:
            return {
                "status": False,
                "error": 1,
                "message": f"File download unsuccessful due to: {e}",
                "data": {}
            }



