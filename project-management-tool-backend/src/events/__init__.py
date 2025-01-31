from src.services import SharepointEmailService
from src.templates import HtmlTemplateService
from .base_event import BaseEvent

class NotificationServiceManager:
    service_type = 'mail'
    
    def __init__(self):
        self.service = SharepointEmailService()
        self.handler_class = None
        
    def __load_template(self):
        template = self.handler_class.TEMPLATE
        data = self.handler_class.DATA
        
        template_service = HtmlTemplateService(template, data)
        template_str = template_service.load_template()
        return template_str
    
    def send(self, handler_class:BaseEvent):
        """
        Get the handler for a given event type.

        Parameters:
        ----------
        handler_class : dict
            The type of event to handle.
        
        emails: list[str]
            the emails is the list of emails that need to be send
        
        data: dict
            the data to be used in the email template

        """
        self.handler_class = handler_class
        
        if not self.handler_class:
            raise ValueError("No handler found for event type")
        
        
        template = self.__load_template()
        
        recipients = [
            {
                "emailAddress": {
                    "address": email
                }
            }
            for email in handler_class.TO 
        ]
        
        email_data = {
            "message": {
                "subject": handler_class.SUBJECT,
                "body": {
                    "contentType": "HTML",
                    "content": template,
                },
                "toRecipients": recipients,
            }
        }
        self.service.set_data(email_data)
        self.service.from_sender()


from .events import Events