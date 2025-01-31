from src.database import db
from src.models import Project
from flask import jsonify

class DisplayProject:
    def __init__(self, request):
        self.request= request
        self.db = db.session()

    def display(self):
        self.body = self.request.json

        query = self.db.query(Project).filter(Project.project_id == self.body['project_id']).first()
        
        project_data = query.get()

        return {
            "status":True,
            "error_code":0,
            "message":"details fetched",
            "data":project_data,
        }