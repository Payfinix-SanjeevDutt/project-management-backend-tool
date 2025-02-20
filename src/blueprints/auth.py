
from flask import Blueprint, request

from src.handlers import CreateEmployee, LoginEmployee, UserVerify, OtpService, AccessTokenHandler, PasswordReset

auth_blueprint = Blueprint("auth",__name__)

@auth_blueprint.route("/sign-up", methods=["POST"])
def employeeCreate():
    return CreateEmployee(request=request).create()

@auth_blueprint.route("/sign-in", methods=["POST"])
def employeeLogin():
    return LoginEmployee(request=request).login()

@auth_blueprint.route("/user-verify", methods=["POST"])
def userVerification():
    return UserVerify(request=request).verify()

@auth_blueprint.route("/me", methods=["GET"])
def authGuard():
    return AccessTokenHandler(request=request).getAccessToken()

@auth_blueprint.route("/reset-password", methods=["POST"])
def resetPassword():
    return PasswordReset(request=request).reset()

@auth_blueprint.route("/otp-resend", methods=["POST"])
def otpResend():
    return OtpService(request=request).resend()

@auth_blueprint.route("/otp-request", methods=["POST"])
def otpRequest():
    return OtpService(request=request).newRequest()

@auth_blueprint.route("/otp-verify", methods=["POST"])
def otpVerify():
    return OtpService(request=request).verify()