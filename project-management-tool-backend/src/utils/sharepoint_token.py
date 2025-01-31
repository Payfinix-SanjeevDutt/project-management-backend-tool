import requests
from src.config import SharePointApi

class SharePointAccess:
    
    def __init__(self):
        self.__payload = {
            'grant_type': 'client_credentials',
            'client_id': SharePointApi.CLIENT_ID,
            'client_secret': SharePointApi.CLIENT_SECRET,
            'scope': SharePointApi.SCOPE
        }
    
    def generate_token(self):
        response = requests.post(SharePointApi.TOKEN_URL, data=self.__payload)
        token_info = response.json()
        access_token = token_info.get('access_token')
        return access_token