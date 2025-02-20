from flask import jsonify
from sqlalchemy import select
from src.database import db
from src.models import Employee
from ..otp.actions import OtpHandler

class OtpService:
    def __init__(self, request) -> None:
        self.request = request
        self.session = db.session()

    def resend(self):
        try:
            body = self.request.json
            
            query = select(Employee).where(Employee.email==body['email'])
            result:Employee | None = self.session.execute(query).scalars().first()
            
            if result == None:
                return jsonify({
                    "status":True,
                    "error_code":3,
                    "message":"user not exists",
                }), 404
            
            hander = OtpHandler(body['email'])
            info = hander.resend_otp()

            if info.code=='DELIVERED':
                return jsonify({
                    "status":True,
                    "error_code":0,
                    "message":f"{info.info}",
                }), 200

            return jsonify({
                    "status":True,
                    "error_code":1,
                    "message":f"{info.info}",
                }), 200
            
        except Exception as e:
            return jsonify({
                "status":False,
                "error_code":2,
                "message":f'{e}',
            }), 500
    

    def newRequest(self):
        try:
            body = self.request.json
            
            query = select(Employee).where(Employee.email==body['email'])
            result:Employee | None = self.session.execute(query).scalars().first()
            
            if result == None:
                return jsonify({
                    "status":True,
                    "error_code":3,
                    "message":"user not exists",
                }), 404
            
            hander = OtpHandler(body['email'])
            info = hander.send_otp()
            if info.code in ('DELIVERED', 'ALREADY_EXISTS'):
                return jsonify({
                    "status":True,
                    "error_code":0,
                    "message":f"{info.info}",
                }), 200

            return jsonify({
                    "status":True,
                    "error_code":1,
                    "message":f"{info.info}",
                }), 200
            
        except Exception as e:
            return jsonify({
                "status":False,
                "error_code":2,
                "message":f'{e}',
            }), 500
    
    def verify(self):
        try:
            body = self.request.json
            
            query = select(Employee).where(Employee.email==body['email'])
            result:Employee | None = self.session.execute(query).scalars().first()
            
            if result == None:
                return jsonify({
                    "status":True,
                    "error_code":3,
                    "message":"user not exists",
                }), 404
            
            hander = OtpHandler(body['email'])
            info = hander.verify_otp(body['otp'])

            if info.code=='VERIFIED':
                return jsonify({
                    "status":True,
                    "error_code":0,
                    "message":f"{info.info}",
                }), 200

            return jsonify({
                    "status":True,
                    "error_code":1,
                    "message":f"{info.info}",
                }), 200
            
        except Exception as e:
            return jsonify({
                "status":False,
                "error_code":2,
                "message":f'{e}',
            }), 500