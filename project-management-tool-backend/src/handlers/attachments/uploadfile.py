from src.services.sharepoint.file_manager.actions import SharepointFileManager
from src.models import Task, Stage, Attachment
from src.utils import get_current_time, generate_unique_key

from src.database import db
from flask import request,jsonify

class UploadFileHandler:

    def __init__(self, request) -> None:
        self.request = request
        self.db = db.session()

    def sendAttachment(self):
        project_id = request.form.get('project_id')
        stage_id = request.form.get('stage_id')
        task_id = request.form.get('task_id')
        subtask_id = request.form.get('subtask_id')

        folder_path_parts = ["Projects"]

        if subtask_id:
            subtask = db.session.query(Task).filter_by(task_id=subtask_id).first()
            if not subtask:
                return jsonify({"status": False, "error_code": 400, "message": "Invalid subtask_id provided"}), 400

            task = subtask
            parent_task_ids = []
            while task.parent_id:
                parent_task_ids.append(task.parent_id)
                task = db.session.query(Task).filter_by(task_id=task.parent_id).first()
                if not task:
                    return jsonify({"status": False, "error_code": 400, "message": "Invalid hierarchy detected: missing parent task"}), 400
            
            parent_task_ids.reverse()
            task_id = task.task_id
            stage = db.session.query(Stage).filter_by(stage_id=task.stage_id).first()
            if not stage:
                return jsonify({"status": False, "error_code": 400, "message": "Stage not found for the top-level task"}), 400

            folder_path_parts.extend([str(stage.project_id), str(stage.stage_id)] + [str(id) for id in parent_task_ids] + [str(subtask_id)])
            project_id, stage_id = stage.project_id, stage.stage_id

        elif task_id:
            task = db.session.query(Task).filter_by(task_id=task_id).first()
            if not task:
                return jsonify({"status": False, "error_code": 400, "message": "Invalid task_id provided"}), 400
            
            stage = db.session.query(Stage).filter_by(stage_id=task.stage_id).first()
            if not stage:
                return jsonify({"status": False, "error_code": 400, "message": "Stage not found for the task"}), 400
            
            folder_path_parts.extend([str(stage.project_id), str(stage.stage_id), str(task_id)])
            project_id, stage_id = stage.project_id, stage.stage_id

        elif stage_id:
            stage = db.session.query(Stage).filter_by(stage_id=stage_id).first()
            if not stage:
                return jsonify({"status": False, "error_code": 400, "message": "Invalid stage_id provided"}), 400
            
            folder_path_parts.extend([str(stage.project_id), str(stage_id)])
            project_id = stage.project_id

        elif project_id:
            folder_path_parts.append(str(project_id))
        else:
            return jsonify({"status": False, "error_code": 400, "message": "No valid identifiers provided to generate folder path"}), 400

        if not project_id:
            return jsonify({"status": False, "error_code": 400, "message": "Missing project_id, unable to generate folder path"}), 400

        folder_path = "/".join(folder_path_parts)

        print("folder_path:", folder_path)

        file = request.files.get('files')
        if not file:
            return jsonify({"status": False, "error_code": 400, "message": "No file found in the request"}), 400

        file_size = file.content_length
        if file_size > 4 * 1024 * 1024:
            sharepoint_manager = SharepointFileManager(request)
            sharepoint_manager.uploadLargeFile(folder_path, file)
        else:
            sharepoint_manager = SharepointFileManager(request)
            sharepoint_manager.uploadSmallFile(folder_path, file)


        file_extension = file.filename.rsplit('.', 1)[-1].lower()

        attachment_id = generate_unique_key()
        project = Attachment(
            project_id=project_id,
            subtask_id=subtask_id,
            task_id=task_id,
            stage_id=stage_id,
            file_name=file.filename,
            file_type=file_extension,
            attachment_id=attachment_id,
        )

        self.db.add(project)
        self.db.commit()

        return jsonify({
            "status": True,
            "error_code": 0,
            "message": "File added successfully"
        }), 200

