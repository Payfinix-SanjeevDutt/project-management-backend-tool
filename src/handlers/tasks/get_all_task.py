from flask import request
from sqlalchemy import select, outerjoin
from sqlalchemy.orm import aliased
from src.database import db
from src.models import Task, Employee, Stage  

class AllTaskHandler:
    def __init__(self):
        self.session = db.session()

    def get_all_tasks(self, request):
        try:
            stage_id = request.args.get("stage_id")  

            if not stage_id:
                return {
                    "status": False,
                    "error_code": 1,
                    "message": "Stage ID is required",
                    "data": {}
                }
            
            project_id = request.args.get("project_id")
            if not project_id:
                return {
                    "status": False,
                    "error_code": 1,
                    "message": "Project ID is required",
                    "data": {}
                }

            reporter_alias = aliased(Employee, name="reporter")
            assignee_alias = aliased(Employee, name="assignee")

            query = (
                select(
                    Task,
                    reporter_alias.name.label("rname"),
                    reporter_alias.avatar.label("ravatar"),
                    reporter_alias.email.label("remail"),
                    assignee_alias.name.label("aname"),
                    assignee_alias.avatar.label("aavatar"),
                    assignee_alias.email.label("aemail"),
                )
                .select_from(Task)
                .outerjoin(reporter_alias, Task.reporter_id == reporter_alias.employee_id)
                .outerjoin(assignee_alias, Task.assignee_id == assignee_alias.employee_id)
                .filter(Task.stage_id == stage_id ,Stage.project_id == project_id)  
            )
            
            result = self.session.execute(query).all()

            tasks = {}
            sub_tasks = {}
            temp_tasks = {}

            for task, rname, ravatar, remail, aname, aavatar, aemail in result:
                data = task.get_details()
                data.update({
                    "reporter_name": rname,
                    "reporter_avatar": ravatar,
                    "reporter_email": remail,
                    "assignee_name": aname,
                    "assignee_avatar": aavatar,
                    "assignee_email": aemail,
                    "children": []
                })
                
                if not data['parent_id']:  
                    tasks[data['task_id']] = data
                else:
                    sub_tasks[data['task_id']] = data
                    if data['parent_id'] not in temp_tasks:
                        temp_tasks[data['parent_id']] = set()
                    temp_tasks[data['parent_id']].add(data['task_id'])
            
            for key, value in temp_tasks.items():
                if key in tasks:  
                    tasks[key]['children'] = list(value)

            return {
                "status": True,
                "error_code": 0,
                "message": "Success",
                "data": {
                    "tasks": tasks,
                    "sub_tasks": sub_tasks
                }
            }

        except Exception as e:
            print(e)
            return {
                "status": False,
                "error_code": 1,
                "message": f"Failed to retrieve tasks due to {e}",
                "data": {}
            }
        

    def get_sprint_task(self, request):
        try:
            body = request.json
            sprint_id = body['sprint_id']
            
            reporter_alias = aliased(Employee, name="reporter")
            assignee_alias = aliased(Employee, name="assignee")

            query = (
                select(
                    Task,
                    reporter_alias.name.label("rname"),
                    reporter_alias.avatar.label("ravatar"),
                    reporter_alias.email.label("remail"),
                    assignee_alias.name.label("aname"),
                    assignee_alias.avatar.label("aavatar"),
                    assignee_alias.email.label("aemail"),
                )
                .select_from(Task)
                .outerjoin(reporter_alias, Task.reporter_id == reporter_alias.employee_id)
                .outerjoin(assignee_alias, Task.assignee_id == assignee_alias.employee_id)
                .filter(Task.sprint_id == sprint_id) 
            )
            
            result = self.session.execute(query).all()

            tasks = []
            for task, rname, ravatar, remail, aname, aavatar, aemail in result:
                data = task.get_details()  
                data.update({
                    "reporter_name": rname,
                    "reporter_avatar": ravatar,
                    "reporter_email": remail,
                    "assignee_name": aname,
                    "assignee_avatar": aavatar,
                    "assignee_email": aemail,
                    "children": []  
                })
                tasks.append(data)
            
            return {
                "status": True,
                "error": 0,
                "data": tasks
            }

        except Exception as e:
            return {
                "status": False,
                "error": 1,
                "message": f"Failed to retrieve tasks due to {e}"
            }

