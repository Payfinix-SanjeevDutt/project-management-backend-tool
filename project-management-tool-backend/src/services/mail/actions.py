import requests
from src.config import SharePointApi
from src.utils import SharePointAccess

class SharepointEmailService:
    
    def __init__(self):
        self.sender_mail = SharePointApi.SENDER_MAIL
        self.access_token = SharePointAccess()
        self.request_data  = None
    
    def set_data(self, data):
        self.request_data = data
        
    def sender_mail(self, mail):
        self.sender_mail = mail
        
    def __generate_headers(self):
        headers = {
            "Authorization": f"Bearer {self.access_token.generate_token()}",
            "Content-Type": "application/json",
        }
        return headers
        
    def from_domain(self):
        response = requests.post(
            SharePointApi.EMAIL_URL,
            headers=self.__generate_headers(),
            json=self.request_data,
        )
        if not response.ok :
            raise Exception(f"unable to deliver email {response.status_code}")
        
    def from_sender(self):
        response = requests.post(
            SharePointApi.EMAIL_URL_V2(self.sender_mail),
            headers=self.__generate_headers(),
            json=self.request_data,
        )
        if not response.ok :
            raise Exception(f"unable to deliver email {response.status_code}")