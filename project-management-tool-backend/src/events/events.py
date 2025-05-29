from .project_events import ProjectAccess, ProjectRole, ProjectDeletion
from .user_events import MailOtp, WelcomeUser
from .base_event import BaseEvent
from .tasks_event import TaskAssigneeAssigned,TaskReporterAssigned,TaskOthersNotified

class Events:
    OTP:MailOtp = MailOtp
    WELCOME_USER:BaseEvent= WelcomeUser
    PROJECT_ACCESS:BaseEvent= ProjectAccess
    PROJECT_ROLE:BaseEvent = ProjectRole
    PROJECT_DELETE:BaseEvent = ProjectDeletion
    ASSIGNEE_ASSIGNED:BaseEvent=TaskAssigneeAssigned
    REPORTER_ASSIGNED:BaseEvent=TaskReporterAssigned
    OTHERS_NOTIFIED:BaseEvent=TaskOthersNotified

    