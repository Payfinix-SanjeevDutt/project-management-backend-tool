# from flask import request
# from sqlalchemy import select
# from sqlalchemy.orm import Session
# from src.database import db
# from src.models import Task 

# class TaskSingleHandler:
#     def __init__(self):
#         self.session: Session = db.session()

#     def get_single_task(self, request):
#         try:
#             body = request.json
            
#             if 'task_id' not in body:
#                 return {
#                     "status": False,
#                     "error": 1,
#                     "message": "task_id is required"
#                 }

#             stmt = select(Task).where(Task.task_id == body["task_id"])
#             result = self.session.execute(stmt).scalar_one_or_none()

#             if result:
#                 return {
#                     "status": True,
#                     "error": 0,
#                     "data": {
#                         "task_id": result.task_id,
#                         "project_id": result.project_id,
#                         "stage_id": result.stage_id,
#                         "reporter_id": result.reporter_id,
#                         "assignee_id": result.assignee_id,
#                         "sprint_id": result.sprint_id,
#                         "task_name": result.task_name,
#                         "description": result.description,
#                         "status": result.status,
#                         "priority": result.priority,
#                         "start_date": result.start_date,
#                         "actual_start_date": result.actual_start_date,
#                         "end_date": result.end_date,
#                         "actual_end_date": result.actual_end_date
#                     }
#                 }
#             else:
#                 return {
#                     "status": False,
#                     "error": 1,
#                     "message": "Task not found"
#                 }
#         except Exception as e:
#             return {
#                 "status": False,
#                 "error": 1,
#                 "message": f"Failed to retrieve task due to {e}"
#             }
#         finally:
#             self.session.close() 

from flask import request, jsonify
from sqlalchemy import select
from sqlalchemy.orm import aliased
from sqlalchemy.exc import NoResultFound
from src.database import db
from src.models import Task, Employee


class TaskSingleHandler:
    def __init__(self):
        self.session = db.session()

    def get_single_task(self,request):
        try:
            body = request.get_json() or {}
            task_id = body.get("task_id")
            stage_id = body.get("stage_id")

            if not task_id or not stage_id:
                return jsonify({
                    "status": False,
                    "error_code": 1,
                    "message": "Both task_id and stage_id are required",
                    "data": {}
                }), 400

            reporter_alias = aliased(Employee, name="reporter")
            assignee_alias = aliased(Employee, name="assignee")

            stmt = (
                select(
                    Task,
                    reporter_alias.name.label("rname"),
                    reporter_alias.avatar.label("ravatar"),
                    reporter_alias.email.label("remail"),
                    assignee_alias.name.label("aname"),
                    assignee_alias.avatar.label("aavatar"),
                    assignee_alias.email.label("aemail"),
                )
                .outerjoin(reporter_alias, Task.reporter_id == reporter_alias.employee_id)
                .outerjoin(assignee_alias, Task.assignee_id == assignee_alias.employee_id)
                .where(Task.task_id == task_id, Task.stage_id == stage_id)
            )

            result = self.session.execute(stmt).one_or_none()

            if not result:
                return jsonify({
                    "status": False,
                    "error_code": 1,
                    "message": "Task not found with the provided task_id and stage_id",
                    "data": {}
                }), 404

            task, rname, ravatar, remail, aname, aavatar, aemail = result

            task_data = task.get_details()
            task_data.update({
                "reporter_name": rname,
                "reporter_avatar": ravatar,
                "reporter_email": remail,
                "assignee_name": aname,
                "assignee_avatar": aavatar,
                "assignee_email": aemail,
                "children": []  
            })

            return jsonify({
                "status": True,
                "error_code": 0,
                "message": "Success",
                "data": task_data
            }), 200

        except NoResultFound:
            return jsonify({
                "status": False,
                "error_code": 1,
                "message": "Task not found with the provided task_id and stage_id",
                "data": {}
            }), 404

        except Exception as e:
            return jsonify({
                "status": False,
                "error_code": 1,
                "message": f"Failed to retrieve task due to: {str(e)}",
                "data": {}
            }), 500

        finally:
            self.session.close()
