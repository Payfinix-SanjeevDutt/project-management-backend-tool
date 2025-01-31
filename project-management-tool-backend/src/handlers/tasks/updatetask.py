from flask import request, jsonify
from sqlalchemy import update, select
from sqlalchemy.exc import NoResultFound
from src.database import db
from src.models import Task, Employee
from datetime import datetime


class TaskUpdateHandler:
    def __init__(self):
        self.session = db.session()

    @staticmethod
    def validate_date(date_str):
        """
        Validates and parses a date string in the format YYYY-MM-DD.
        Returns a date object if valid, otherwise None.
        """
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            return None

    def update_task(self, request):
        try:
            # Parse request body
            body = request.get_json() or {}
            task_id = body.get("task_id")
            stage_id = body.get("stage_id")
            status = body.get("status")
            assignee_id = body.get("assignee_id")
            reporter_id = body.get("reporter_id")
            priority = body.get("priority")
            start_date = body.get("start_date")
            end_date = body.get("end_date")
            actual_start_date = body.get("actual_start_date")
            actual_end_date = body.get("actual_end_date")

            # Validate required fields
            if not task_id or not stage_id:
                return jsonify({
                    "status": False,
                    "error_code": 1,
                    "message": "Both task_id and stage_id are required",
                    "data": {}
                }), 400

            # Check if task exists
            stmt = select(Task).where(Task.task_id == task_id, Task.stage_id == stage_id)
            task = self.session.execute(stmt).scalar_one_or_none()
            if not task:
                return jsonify({
                    "status": False,
                    "error_code": 1,
                    "message": "Task not found with the provided task_id and stage_id",
                    "data": {}
                }), 404

            # Prepare the update data
            update_data = {}

            if status:
                update_data["status"] = status

            if assignee_id:
                # Validate assignee existence
                assignee_exists = self.session.query(Employee).filter(Employee.employee_id == assignee_id).one_or_none()
                if not assignee_exists:
                    return jsonify({
                        "status": False,
                        "error_code": 1,
                        "message": f"Invalid assignee_id: {assignee_id}. Assignee does not exist.",
                        "data": {}
                    }), 404
                update_data["assignee_id"] = assignee_id

            if reporter_id:
                # Validate reporter existence
                reporter_exists = self.session.query(Employee).filter(Employee.employee_id == reporter_id).one_or_none()
                if not reporter_exists:
                    return jsonify({
                        "status": False,
                        "error_code": 1,
                        "message": f"Invalid reporter_id: {reporter_id}. Reporter does not exist.",
                        "data": {}
                    }), 404
                update_data["reporter_id"] = reporter_id

            if priority:
                update_data["priority"] = priority

            # Validate and add date fields
            if start_date:
                validated_date = self.validate_date(start_date)
                if validated_date:
                    update_data["start_date"] = validated_date
                else:
                    return jsonify({
                        "status": False,
                        "error_code": 1,
                        "message": "Invalid start_date format. Use YYYY-MM-DD.",
                        "data": {}
                    }), 400

            if end_date:
                validated_date = self.validate_date(end_date)
                if validated_date:
                    update_data["end_date"] = validated_date
                else:
                    return jsonify({
                        "status": False,
                        "error_code": 1,
                        "message": "Invalid end_date format. Use YYYY-MM-DD.",
                        "data": {}
                    }), 400

            if actual_start_date:
                validated_date = self.validate_date(actual_start_date)
                if validated_date:
                    update_data["actual_start_date"] = validated_date
                else:
                    return jsonify({
                        "status": False,
                        "error_code": 1,
                        "message": "Invalid actual_start_date format. Use YYYY-MM-DD.",
                        "data": {}
                    }), 400

            if actual_end_date:
                validated_date = self.validate_date(actual_end_date)
                if validated_date:
                    update_data["actual_end_date"] = validated_date
                else:
                    return jsonify({
                        "status": False,
                        "error_code": 1,
                        "message": "Invalid actual_end_date format. Use YYYY-MM-DD.",
                        "data": {}
                    }), 400

            # Check if there's anything to update
            if not update_data:
                return jsonify({
                    "status": False,
                    "error_code": 1,
                    "message": "No valid fields provided for update",
                    "data": {}
                }), 400

            # Execute the update
            stmt_update = (
                update(Task)
                .where(Task.task_id == task_id, Task.stage_id == stage_id)
                .values(**update_data)
            )
            self.session.execute(stmt_update)
            self.session.commit()

            return jsonify({
                "status": True,
                "error_code": 0,
                "message": "Task updated successfully",
                "data": {"task_id": task_id, "updated_fields": list(update_data.keys())}
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
                "message": f"Failed to update task due to: {str(e)}",
                "data": {}
            }), 500

        finally:
            self.session.close()
