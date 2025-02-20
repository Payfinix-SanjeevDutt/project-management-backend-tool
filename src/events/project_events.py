from src.templates import HtmlTemplates
from .base_event import BaseEvent



class ProjectAccess(BaseEvent):
    TEMPLATE = HtmlTemplates.PROJECT_ACCESS
    SUBJECT = 'Access to project'
    TYPE = 'PROJECT_ACCESS'
    TO = []
    DATA = {}
    
    def __init__(self, user_name:str="", project_name:str="", access:str='GRANT', emails:list[str]=[]):
        self.TO = emails
        self.DATA = {
            "user_name":user_name,
            "project_name":project_name,
            "access":access
        }

class ProjectRole(BaseEvent):
    TEMPLATE = HtmlTemplates.PROJECT_ROLES
    SUBJECT = 'New role in project'
    TYPE = 'PROJECT_ROLE'
    TO = []
    DATA = {}
    
    __ROLES = {
        "ADMIN":{
            "responsibilities": [
                "Manage project settings, teams, and user roles.",
                "Ensure smooth operation of the tool by troubleshooting and handling escalations.",
                "Monitor project progress and oversee resource allocation.",
                "Customize workflows, permissions, and integrations."
            ],
            "access": [
                "Full access to all projects and settings.",
                "Can create, update, or delete projects.",
                "Control user roles and permissions.",
                "Access all reports, dashboards, and audit logs."
            ]
        },
        "PROJECT_LEAD":{
            "responsibilities": [
                "Plan and oversee the project lifecycle, from initiation to completion.",
                "Assign tasks, set deadlines, and monitor progress.",
                "Ensure team alignment with project goals.",
                "Collaborate with stakeholders to manage priorities and risks."
            ],
            "access": [
                "Can create and manage tasks within the assigned project.",
                "View and edit project timelines, resources, and dependencies.",
                "Access team performance metrics and project reports.",
                "Manage project-specific permissions but not overall settings."
            ]
        },
        "ASSIGNEE":{
            "responsibilities": [
                "Complete tasks assigned to them on time.",
                "Provide regular updates on progress and flag roadblocks.",
                "Collaborate with team members to resolve issues.",
                "Ensure quality in the deliverables assigned to them."
            ],
            "access": [
                "View assigned tasks and subtasks.",
                "Add comments, attach files, and update task statuses.",
                "Cannot create or modify tasks they’re not assigned to.",
                "Limited access to reports, only related to their work."
            ]
        },
        "REPORTER":{
            "responsibilities": [
                "Log and report issues, bugs, or concerns to the team.",
                "Track the status of reported issues and provide additional context when needed.",
                "Assist in testing and verifying issue resolutions.",
                "Provide feedback to improve workflows."
            ],
            "access": [
                "Can create and view issues or tickets.",
                "View the status and updates of the issues they’ve reported.",
                "Cannot modify tasks, timelines, or other project settings.",
                "Access limited to the reporting module."
            ]
        }
    }

    def __init__(self, user_name:str="", project_name:str="", role:str='ADMIN', emails:list[str]=[]):
        self.TO = emails
        self.DATA = {
            "user_name":user_name,
            "project_name":project_name,
            "role":role,
            "responsibilities":self.__ROLES[role]['responsibilities'],
            "access":self.__ROLES[role]['access']
        }

class ProjectAccess(BaseEvent):
    TEMPLATE = HtmlTemplates.PROJECT_INVITE
    SUBJECT = 'Invitaion to project'
    TYPE = 'PROJECT_INVITE'
    TO = []
    DATA = {}
    
    def __init__(self, user_name:str="", project_name:str="", cover_image:str='', link:str="", emails:list[str]=[]):
        self.TO = emails
        self.DATA = {
            "user_name":user_name,
            "project_name":project_name,
            "cover_image":cover_image,
            "link":link
        }


class ProjectDeletion(BaseEvent):
    TEMPLATE = HtmlTemplates.PROJECT_DELETE
    SUBJECT = 'Project is been deleted'
    TYPE = 'PROJECT_DELETE'
    TO = []
    DATA = {}
    
    def __init__(self, user_name:str="", project_name:str="", deleted_date:str="", deleted_by:str='', reason:str="", emails:list[str]=[]):
        self.TO = emails
        self.DATA = {
            "user_name":user_name,
            "project_name":project_name,
            "deleted_by":deleted_by,
            "deleted_date":deleted_date,
            "reason":reason
        }