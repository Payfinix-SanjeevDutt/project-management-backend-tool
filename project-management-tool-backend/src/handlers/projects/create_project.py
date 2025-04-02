from src.database import db
from src.models import Project, ProjectUsers, UsersRole, UserAccess, Stage, Task
from src.utils import get_current_time, generate_unique_key
from flask import jsonify
from src.services.sharepoint.file_manager.actions import SharepointFileManager


class CreateProject:
    def __init__(self, request):
        self.request = request
        self.db = db.session()

    def get_defaults(self):
        default_values = {
            'Estimation': {'CMMI':{'Estimation method complexity point': {}, 'Project schedule': {}}},
            'Project Management': {
                'CMMI':{
                'MOM': {},
                'Project Planning, Monitoring and Control': {},
                'Time Tracker': {},
                'Senior management review report': {},
                'Sign off': {},
                'Closure report': {},
                'formal evaluation form': {},
                'Master PMP': {},
                'Project Level PMP & tracking': {}},
                'CAR-CMMI':{'Review Defects':{},'Test Defects':{}},
                'Review Report-CMMI': {'Reviews': {}},
            },
            'Requirements': {
                'CMMI':{'Requirement Traceabality Matrix': {},
                'Software Requirement Specification': {},
                'Query Log': {},
                'Technical Design Documentation': {},
                'Design Screens': {},
                'Design Sign-Off': {}
            }},
            'Coding': {
                'CMMI':{'Test Plan': {},
                'Defects System Testing': {},
                'Unit testing': {},
                'System test cases': {},
                'Unit test cases': {},
                'Unit defects log': {},
                'Validation report': {}
            }},
            'Testing': {
                'CMMI':{'Validation Test Case': {},
                'Test Plan': {},
                'Validation Log': {},
                'Validation Report': {},
            }},
            'Deployment': {
               'CMMI':{'Release Notes': {}},
            },
            'UAT': {
               'CMMI':{'Test Trials': {}},
            },
        }
        return default_values

    def create_default_objects(self, project_id, body):
        obj_arr = []
        for stage, tasks in self.get_defaults().items():
            stage_id = generate_unique_key()
            stage = Stage(
                stage_id=stage_id,
                name=stage,
                project_id=project_id,
                start_date=body['start_date'],
                end_date=body['end_date'],
                actual_start_date=None,
                actual_end_date=None
            )
            obj_arr.append(stage)
            for task, subtasks in tasks.items():
                task_id = generate_unique_key()
                task_object = Task(
                    task_id=task_id,
                    task_name=task,
                    stage_id=stage_id,
                    sprint_id=None,
                    project_id=body['project_id'],
                    parent_id=None
                )
                obj_arr.append(task_object)
                for subtask in subtasks.keys():
                    subtask_id = generate_unique_key()
                    subtask_object = Task(
                        task_id=subtask_id,
                        task_name=subtask,
                        stage_id=stage_id,
                        sprint_id=None,
                        project_id=body['project_id'],
                        parent_id=task_id
                    )
                    obj_arr.append(subtask_object)

        return obj_arr

    def create_project(self, project_id, body):
        project = Project(
            project_id=project_id,
            name=body['name'],
            status=body['status'],
            description=body['description'],
            start_date=body['start_date'],
            end_date=body['end_date'],
            actual_start_date=body['actual_start_date'],
            actual_end_date=body['actual_end_date'],
            cover_img=body['cover_img']
        )

        project_users = ProjectUsers(
            project_id=project_id,
            employee_id=body['employee_id'],
            role=UsersRole.ADMIN,
            last_active=get_current_time(),
            access_status=UserAccess.GRANT
        )
        return [project, project_users]

    def create(self):
        try:
            body = self.request.json
            print(body)

            project_id = generate_unique_key()

            projects = self.create_project(project_id, body)
            default_creation = self.create_default_objects(project_id, body)
            projects.extend(default_creation)
            self.db.add_all(projects)
            self.db.commit()

            requestData = {
                "folder_name": project_id,
                "path": "Projects"
            }
            project_folder = SharepointFileManager(requestData).createFolder()

            return jsonify({
                "status": True,
                "error_code": 0,
                "message": "Project created successfully",
                "data": {
                    "project_id": project_id
                }
            }), 200

        except Exception as e:
            print(e)
            return jsonify({
                "status": False,
                "error_code": 2,
                "message": f"Project is not created{e}"
            }), 500
