from flask import request, jsonify
from sqlalchemy import update
from sqlalchemy.orm import Session
from src.database import db
from src.models import Sprint
from datetime import datetime

class SprintUpdateHandler:
    def __init__(self):
        self.session: Session = db.session()

    def convert_date_format(self, date_str):
        return datetime.strptime(date_str, '%d-%m-%y %I:%M %p')

    def sprint_update(self, request):
        try:
            body = request.json
            
            existing_sprint = self.session.query(Sprint).filter(Sprint.sprint_id == body['sprint_id']).first()
            if not existing_sprint:
                return {
                    "status": False,
                    "error": 1,
                    "message": "Sprint ID not found"
                }

            stmt = (
                update(Sprint)
                .where(Sprint.sprint_id == body['sprint_id'])
                .values(**body)
            )

            self.session.execute(stmt)
            self.session.commit()
            return {
                "status": True,
                "error": 0,
                "message": "Sprint updated successfully"
            }
        except Exception as e:
            self.session.rollback()  
            return {
                "status": False,
                "error": 1,
                "message": f"Sprint update unsuccessful due to {e}"
            }
        

    def update_sprint_dates(self, request):
        data = request.json

        sprint_id = data.get('sprint_id')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        try:
        
            # Convert dates to datetime objects
            formatted_start_date = self.convert_date_format(start_date) if start_date else None
            formatted_end_date = self.convert_date_format(end_date) if end_date else None

            # Query the Sprint by ID
            sprint = Sprint.query.filter_by(sprint_id=sprint_id).first()

            if not sprint:
                return jsonify({
                    "status": False,
                    "error": 1,
                    "message": "Sprint Not Found"
                }), 404

            # Update the sprint dates
            sprint.start_date = formatted_start_date
            sprint.end_date = formatted_end_date

            self.session.commit()
            
            return jsonify({
                "status": True,
                "error": 0,
                "message": "Sprint dates updated successfully",
                "data": {
                    "start_date": sprint.start_date,
                    "end_date": sprint.end_date
                }
            })
        except Exception as e:
            self.session.rollback()
            return jsonify({
                "status": False,
                "error": 1,
                "message": f"Sprint update unsuccessful due to {e}",
            }), 500

        
