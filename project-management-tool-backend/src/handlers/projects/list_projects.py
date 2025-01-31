from src.database import db
from sqlalchemy import select, and_
from src.models import Project, ProjectUsers, Employee


class ListProject:
    def __init__(self, request):
        self.request = request
        self.db = db.session()

    def format_date(self, item):
        if item:
            item = item.strftime("%m-%d-%Y")
        return item

    def list(self):
        try:
            body = self.request.json

            query = select(
                Project.project_id,
                Project.name,
                Project.status,
                Project.start_date,
                Project.end_date,
                Project.actual_start_date,
                Project.actual_end_date,
                Project.cover_img,
                Employee.name,
                Employee.email,
                Employee.avatar,
                Employee.employee_id
            ).\
                join(ProjectUsers, and_(Project.project_id == ProjectUsers.project_id, ProjectUsers.role == 'ADMIN'), isouter=True).\
                join(Employee, ProjectUsers.employee_id == Employee.employee_id, isouter=True).\
                where(Project.project_id.in_(select(ProjectUsers.project_id).where(
                    ProjectUsers.employee_id == body['employee_id'])))
            

            result = self.db.execute(query).all()
            response = []

            for item in result:
                response.append({
                    "id": item[0],
                    "name": item[1],
                    "status": item[2],
                    "start_date": self.format_date(item[3]),
                    "end_date": self.format_date(item[4]),
                    "actual_start_date": self.format_date(item[5]),
                    "actual_end_date": self.format_date(item[6]),
                    "cover_img": item[7],
                    'lead_name': item[8],
                    'lead_email': item[9],
                    'lead_avatar': item[10],
                    "lead_id": item[11],
                })

            return {
                "status": True,
                "error_code": 0,
                "message": 'project fetched succesful',
                "data": response
            }

        except Exception as e:
            print(e)
            return {
                "status": False,
                "error_code": 1,
                "message": f'failed {e}',
                "data": []
            }
