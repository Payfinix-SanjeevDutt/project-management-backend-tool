from src.templates import HtmlTemplates
from .base_event import BaseEvent

class MailOtp(BaseEvent):
    TEMPLATE = HtmlTemplates.VERIFY_OTP
    SUBJECT = 'Verify your email address'
    TYPE = 'OTP'
    TO = []
    DATA = {}
    
    def __init__(self, otp:str="", emails:list[str]=[]):
        self.TO = emails
        self.DATA = {
            "otp":otp
        }

class WelcomeUser(BaseEvent):
    TEMPLATE = HtmlTemplates.WELCOME_USER
    SUBJECT = 'Welcome to our platform'
    TYPE = 'WELCOME_USER'
    TO = []
    DATA = {}
    
    def __init__(self, user_name:str="", emails:list[str]=[]):
        self.TO = emails
        self.DATA = {
            "user_name":user_name
        }