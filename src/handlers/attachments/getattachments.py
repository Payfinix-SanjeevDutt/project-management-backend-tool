from flask import request
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.services.sharepoint.file_manager.actions import SharepointFileManager
from src.database import db
from src.models import Attachment


class GetAllAttachments:
    def __init__(self, request):
        self.session = db.session()
        self.request = request


    def get_attached_files(self):
        try:
            data = request.get_json()  
            project_id = data.get('project_id')
            stage_id = data.get('stage_id')
            task_id = data.get('task_id')
            subtask_id = data.get('subtask_id')

            print("body>>>", task_id)
            if not any([project_id, stage_id, task_id, subtask_id]):
                return {
                    "status": False,
                    "error": 1,
                    "message": "At least one identifier (project_id, stage_id, task_id, or subtask_id) is required."
                }

            stmt = select(Attachment)
            if project_id:
                stmt = stmt.where(Attachment.project_id == project_id, Attachment.stage_id == None, Attachment.task_id == None,
                                  Attachment.subtask_id == None)
            if stage_id:
                stmt = stmt.where(Attachment.stage_id == stage_id, Attachment.task_id == None,
                                  Attachment.subtask_id == None)
            if task_id:
                stmt = stmt.where(Attachment.task_id == task_id,  Attachment.subtask_id == None)
            if subtask_id:
                stmt = stmt.where(Attachment.subtask_id == subtask_id)
            result = self.session.execute(stmt).scalars().all()

            attachments = []
            for attachment in result:
                attachments.append({
                    "attachment_id": attachment.attachment_id,
                    "file_name": attachment.file_name,
                    "file_type": attachment.file_type,
                    "project_id": attachment.project_id,
                    "stage_id": attachment.stage_id,
                    "subtask_id": attachment.subtask_id,
                    "task_id": attachment.task_id,
                })


            if attachments:
                folder_path_parts = ["Projects"]
                first_attachment = attachments[0]
                if first_attachment.get("project_id"):
                    folder_path_parts.append(first_attachment["project_id"])
                if first_attachment.get("stage_id"):
                    folder_path_parts.append(first_attachment["stage_id"])
                if first_attachment.get("task_id"):
                    folder_path_parts.append(first_attachment["task_id"])
                if first_attachment.get("subtask_id"):
                    folder_path_parts.append(first_attachment["subtask_id"])

                folder_path = "/".join(folder_path_parts)

                print("folder_path", folder_path)

                folder_data_response = SharepointFileManager(request)
                folder_files_response = folder_data_response.get_folder_data(folder_path)
                print("folder_files_response raw:", folder_files_response)

            folder_files = folder_files_response.get('files', []) if folder_files_response else []

            combined_data = {
                "database_attachments": attachments,
                "folder_files": folder_files,
                "folder_path": folder_path
            }

            return {
                "status": True,
                "error": 0,
                "data": combined_data
            }

        except Exception as e:
            return {
                "status": False,
                "error": 1,
                "message": f"Failed to retrieve attachments: {e}"
            }



