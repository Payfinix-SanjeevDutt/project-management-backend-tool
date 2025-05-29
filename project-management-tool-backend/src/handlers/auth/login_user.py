import requests
from flask import redirect, jsonify
from src.config.microsoftauth import MicrosoftAuthApi
from src.models import Employee
from src.database import db
from src.utils import generate_token

AUTH_URL = "https://login.microsoftonline.com/common/oauth2/v2.0/authorize"
TOKEN_URL = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
USER_INFO_URL = "https://graph.microsoft.com/v1.0/me"


class LoginEmployee:
    def __init__(self, request) -> None:
        self.request = request
        self.session = db.session()

    def login(self):
        try:
            body = self.request.json
            email = body.get('email')
            password = body.get('password')

            employee = self.session.query(Employee).filter_by(email=email, password=password).first()
            if employee:
                return jsonify({
                    "status": True,
                    "error_code": 0,
                    "message": "User login successfully",
                    "data":{
                        "accessToken": generate_token(employee_id = employee.employee_id)  
                    }
                }), 200
            else:
                return jsonify({
                    "status": False,
                    "error_code": 1,
                    "message": "Invalid email or password",
                    "data":{
                        "accessToken":""
                    }
                }), 401

        except Exception as e:
            print(e)
            return jsonify({
                "status":False,
                "error_code":2,
                "message":f'error in login',
                "data":{
                    "accessToken":""   
                }
            }), 500

    def microsoft_login(self):
        try:
            print("Starteddd login api")
            params = {
                "client_id": MicrosoftAuthApi.MICROSOFT_CLIENT_ID,
                "response_type": "code",
                "redirect_uri": MicrosoftAuthApi.MICROSOFT_REDIRECT_URI,
                "response_mode": "query",
                "scope": "User.Read",
                "prompt": "select_account"
            }
            print("params", params)
            login_url = requests.Request(
                'GET', AUTH_URL, params=params).prepare().url
            print("🔁 Redirecting to Microsoft with:", login_url)
            return redirect(login_url)

        except Exception as e:
            return jsonify({
                "status": False,
                "error_code": 3,
                "message": f"Login initiation failed: {str(e)}"
            }), 500

    def microsoft_callback(self):
        try:
            print("starteddddddddddddddddd")
            code = self.request.args.get("code")
            if not code:
                return jsonify({
                    "status": False,
                    "error_code": 4,
                    "message": "Authorization failed: no code received"
                }), 400

            token_data = {
                "client_id": MicrosoftAuthApi.MICROSOFT_CLIENT_ID,
                "client_secret": MicrosoftAuthApi.MICROSOFT_CLIENT_SECRET,
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": MicrosoftAuthApi.MICROSOFT_REDIRECT_URI,
            }

            token_response = requests.post(TOKEN_URL, data=token_data)
            print("TOKEN RESPONSE STATUS:", token_response.status_code)
            print("TOKEN RESPONSE TEXT:", token_response.text)
            token_response.raise_for_status()
            token_json = token_response.json()
            access_token = token_json.get("access_token")

            if not access_token:
                return jsonify({
                    "status": False,
                    "error_code": 5,
                    "message": "Token exchange failed"
                }), 400

            headers = {"Authorization": f"Bearer {access_token}"}
            profile_response = requests.get(USER_INFO_URL, headers=headers)
            profile_response.raise_for_status()
            profile = profile_response.json()
            print("profiledata", profile)

            email = profile.get("userPrincipalName")

            if not email:
                return jsonify({
                    "status": False,
                    "error_code": 6,
                    "message": "Email not found in Microsoft profile"
                }), 400

            # Validate Microsoft email against Employee DB
            employee = self.session.query(
                Employee).filter_by(email=email).first()
            if employee:
                print("suucees validation")
                access_token_internal = generate_token(employee_id=employee.employee_id)
                print("access_token",access_token_internal)
                redirect_url = f"{MicrosoftAuthApi.FRONTEND_BASE_URL}/auth/success?token={access_token_internal}&redirect=/main/dashboard/user-dashboard"
                return redirect(redirect_url)

            else:
                error_msg = "Microsoft account not linked to any employee"
                redirect_url = f"{MicrosoftAuthApi.FRONTEND_BASE_URL}/auth/sign-in?error={error_msg}"
                return redirect(redirect_url)

        except requests.exceptions.RequestException as req_err:
            return jsonify({
                "status": False,
                "error_code": 8,
                "message": f"Request error: {str(req_err)}"
            }), 500
        except Exception as e:
            return jsonify({
                "status": False,
                "error_code": 9,
                "message": f"Callback failed: {str(e)}"
            }), 500





# class LoginEmployee:
#     def __init__(self, request) -> None:
#         self.request = request
#         self.session = db.session()

#     def login(self):
#         try:
#             body = self.request.json
#             email = body.get('email')
#             password = body.get('password')

#             employee = self.session.query(Employee).filter_by(email=email, password=password).first()
#             if employee:
#                 return jsonify({
#                     "status": True,
#                     "error_code": 0,
#                     "message": "User login successfully",
#                     "data":{
#                         "accessToken": generate_token(employee_id = employee.employee_id)
#                     }
#                 }), 200
#             else:
#                 return jsonify({
#                     "status": False,
#                     "error_code": 1,
#                     "message": "Invalid email or password",
#                     "data":{
#                         "accessToken":""
#                     }
#                 }), 401

#         except Exception as e:
#             print(e)
#             return jsonify({
#                 "status":False,
#                 "error_code":2,
#                 "message":f'error in login',
#                 "data":{
#                     "accessToken":""
#                 }
#             }), 500
