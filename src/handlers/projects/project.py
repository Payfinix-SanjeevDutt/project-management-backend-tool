from src.database import db
from sqlalchemy import select,update,delete
from flask import jsonify

from src.models import Project


class projecthandler:
    def __init__(self, request) -> None:
        self.request = request
        self.body = None
        self.session = db.session()
    def getproject(self):
        try:
            stmt = select(Project)
            result = self.session.execute(stmt).all()
            response =[ {
                "project_id":proj.project_id,
                "name":proj.name,
                "status":proj.status,
                "description":proj.description,
                "start_date":proj.start_date,
                "end_date":proj.end_date,
                "actual_start_date":proj.actual_start_date,
                "actual_end_date" : proj.actual_end_date
            } for proj, in result]
            return{
                "status":True,
                "error":0,
                "data":response,
                "message":" project details are dispplayed successfully"
            }
        except Exception as e:
            return{
                "status":False,
                "error":5,
                "data":[],
                "message":f'orders dislpay failed as {e}'
            }
        
    def createproject(self):
        try:
            body = self.request.json
            project = Project(
                project_id=body['project_id'],
                name=body['name'],
                status=body['status'],
                description=body['description'],
                start_date = body['start_date'],
                end_date = body['end_date'],
                actual_start_date = body['actual_start_date'],
                actual_end_date = body['actual_end_date'],
                coverImg = body['coverImg']
            )    
            self.session.add(project)
            self.session.commit()
            return {
                "status":True,
                "error":0,
                "message":"project added succesfully"
            }
            
        except Exception as e:
            return {
                "status":False,
                "error":5,
                "message":f'project dislpay failed as {e}'
            }  
        
    def delete_project(self):
        self.body = self.request.json
        isValidate = self.validateProject()
        if not isValidate:
            response = {
                "message":"id not found",
                "errorcode":6
            }
            return jsonify(response)
        
        statement = delete(Project).where(Project.project_id == self.body['project_id'])
        print(statement)
        self.session.execute(statement)
        self.session.commit()

        return jsonify({
            "message":"project deleted",
            "errorcode":00
        })
    def __init__(self, request=None, info=None) -> None:
        self.request = request
        self.session = db.session()

    
    def validateProject(self):
        if "project_id" not in self.body:
           return False
        return True
    
    # =====================================================
    
    def validateProject(self):
        if "project_id" not in self.body:
           return False
        return True

    def update_project(self):
        self.body = self.request.json
        updateproduct = update(Project).where(Project.project_id == self.body['project_id']).values(**self.body)
        self.session.execute(updateproduct)
        self.session.commit()

        return jsonify({
            "message":"project udated",
            "errorcode":00
        })


          

