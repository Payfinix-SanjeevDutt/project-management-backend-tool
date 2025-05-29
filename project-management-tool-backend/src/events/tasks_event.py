from src.templates import HtmlTemplates
from .base_event import BaseEvent



class TaskAssigneeAssigned(BaseEvent):
    TEMPLATE = HtmlTemplates.ASSIGNEE_ASSIGNED
    SUBJECT = 'New Task Assigned'
    TYPE = 'TASK_ASSIGN'
    TO = []
    DATA = {}
        
    def __init__(self, user_name:str="", project_name:str="", email=[],stage="",task_name="",link=""):
        self.TO = email
        self.DATA = {
            "user_name":user_name,
            "project_name":project_name,
            "stage":stage,
            "task_name":task_name,
            "email":email,
            "link":link
        }


class TaskReporterAssigned(BaseEvent):
    TEMPLATE = HtmlTemplates.REPORTER_ASSIGNED
    SUBJECT = 'New Task Assigned'
    TYPE = 'TASK_ASSIGN'
    TO = []
    DATA = {}
    
    def __init__(self, user_name:str="", project_name:str="", email="",stage="",task_name="",link=""):
        self.TO = email
        self.DATA = {
            "user_name":user_name,
            "project_name":project_name,
            "stage":stage,
            "task_name":task_name,
            "project_name":project_name,
            "link":link
        }
        
class TaskOthersNotified(BaseEvent):
    TEMPLATE = HtmlTemplates.OTHERS_NOTIFIED
    SUBJECT = 'An employee has been assigned'
    TYPE = 'TASK_ASSIGN'
    TO = []
    DATA = {}
        
    def __init__(self, user_name:str="", project_name:str="", email=[],stage="",task_name="",link=""):
        self.TO = email
        self.DATA = {
            "user_name":user_name,
            "project_name":project_name,
            "stage":stage,
            "task_name":task_name,
            "email":email,
            "link":link
        }