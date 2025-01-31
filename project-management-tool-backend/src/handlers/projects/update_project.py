from src.database import db
from src.models import Project
from sqlalchemy import update
from flask import jsonify


class UpdateProject:
    def __init__(self,request):
        self.request = request
        self.db = db.session()

    def update(self):

        try:
            self.body = self.request.json
            

            query = update(Project).where(Project.project_id == self.body['project_id']).values(
                name = self.body.get('name'),
                status = self.body.get('status'),
                description = self.body.get('description'),
                start_date = self.body.get('start_date'),
                end_date = self.body.get('end_date'),
                actual_start_date = self.body.get('actual_start_date'),
                actual_end_date = self.body.get('actual_end_date')
            )
           

            result = self.db.execute(query)
            print(result)
            self.db.commit()

            return jsonify({
                    "error_code":0,
                    "status":True,
                    "message":"successful"
                })
        
        except Exception as e:
            print(e)
            return jsonify({
                "error_code":1,
                "status":False,
                "message":f'error in project update',
                
            })
    