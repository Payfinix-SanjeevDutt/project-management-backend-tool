from flask import Flask, request, jsonify
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from src.database import db
from src.models import Comments, History, Employee
from src.utils import get_current_time


class CommentHandler:
    def __init__(self):
        self.session = db.session()

    def add_to_history(self, task_id, employee_id, description, timestamp):
        try:
            new_history = History(
                task_id=task_id,
                employee_id=employee_id,
                description=description,
                timestamp=timestamp
            )
            self.session.add(new_history)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise Exception(f"Failed to save history: {e}")

    def process_data(self):
        if request.method == 'GET':
            try:
                comments = (
                    self.session.query(Comments)
                    .join(Employee, Comments.employee_id == Employee.employee_id)
                    .all()
                )
                response = [
                    {
                        "comment_id": comment.comment_id,
                        "employee_id": comment.employee_id,
                        "task_id": comment.task_id,
                        "employee_name": comment.employee.name,  
                        "avatar": comment.employee.avatar, 
                        "date": comment.date.strftime("%Y-%m-%d %H:%M:%S"),
                        "action": comment.action,
                        "value": comment.value,
                    }
                    for comment in comments
                ]
                return jsonify(response), 200
            except SQLAlchemyError as e:
                self.session.rollback()
                return jsonify({"error": str(e)}), 500

        if request.method == 'POST':
            data = request.json
            if not data or 'employee_id' not in data or 'task_id' not in data or 'value' not in data:
                return jsonify({"error": "Invalid input"}), 400

            try:
                new_comment = Comments(
                    employee_id=data['employee_id'],
                    task_id=data['task_id'],
                    action=data.get('action', 'COMMENT'),
                    value=data['value'],
                )
                self.session.add(new_comment)
                self.session.commit()

                employee = self.session.query(Employee).filter_by(employee_id=data['employee_id']).first()
                if not employee:
                    return jsonify({"error": "Employee not found"}), 404

                self.add_to_history(
                    task_id=new_comment.task_id,
                    employee_id=new_comment.employee_id,
                    description=f"{employee.name} added a comment :  {new_comment.value}",  # Corrected field
                    timestamp=new_comment.date.strftime("%Y-%m-%d %H:%M:%S")
                )

                response = {
                    "comment_id": new_comment.comment_id,
                    "employee_id": new_comment.employee_id,
                    "task_id": new_comment.task_id,
                    "employee_name": employee.name,  
                    "avatar": employee.avatar,
                    "date": new_comment.date.strftime("%Y-%m-%d %H:%M:%S"),
                    "action": new_comment.action,
                    "value": new_comment.value,
                }
                return jsonify(response), 201
            except SQLAlchemyError as e:
                self.session.rollback()
                return jsonify({"error": str(e)}), 500

    def perform_action(self, request):
        data = request.json
        if not data or 'task_id' not in data or 'action' not in data or 'old_value' not in data or 'new_value' not in data:
            return jsonify({"error": "Invalid input"}), 400

        try:
            task_id = data['task_id']
            employee_id = data.get('employee_id')

            if not employee_id:
                return jsonify({"error": "Employee ID is required"}), 400

            employee = self.session.query(Employee).filter_by(employee_id=employee_id).first()

            if not employee:
                return jsonify({"error": "Employee not found"}), 404

            action_description = f"{employee.name} changed {data['action']} from {data['old_value']} to {data['new_value']}"

            current_time = get_current_time()
            formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S") if not isinstance(current_time, str) else current_time

            self.add_to_history(
                task_id=task_id,
                employee_id=employee_id,
                description=action_description,
                timestamp=formatted_time
            )

            return jsonify({"message": "Action performed successfully", "description": action_description}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def get_history(self, request):
        try:
            history_records = (
                self.session.query(History, Employee) 
                .join(Employee, History.employee_id == Employee.employee_id)
                .order_by(History.timestamp.desc())
                .all()
            )
            response = [
                {
                    "history_id": record[0].history_id, 
                    "task_id": record[0].task_id,
                    "timestamp": record[0].timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    "employee_id": record[1].employee_id, 
                    "employee_name": record[1].name,
                    "avatar": record[1].avatar,
                    "description": record[0].description,
                }
                for record in history_records
            ]
            return jsonify(response), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
