from .loadenv import get_env_variable


class SharePointApi:
    SENDER_MAIL:str = get_env_variable('SHAREPOINT_SENDER_MAIL')
    CLIENT_SECRET:str = get_env_variable('SHAREPOINT_CLIENT_SECRET')
    CLIENT_ID:str = get_env_variable('SHAREPOINT_CLIENT_ID')
    DIR_TENANT_ID:str = get_env_variable('SHAREPOINT_DIR_TENANT_ID')
    DRIVE_ID:str = get_env_variable('SHAREPOINT_DRIVE_ID')
    SCOPE:str = get_env_variable('SHAREPOINT_SCOPE')
    TOKEN_URL:str = f"https://login.microsoftonline.com/{DIR_TENANT_ID}/oauth2/v2.0/token"
    BASE_URL:str = f"https://graph.microsoft.com/v1.0/drives/{DRIVE_ID}/root:/"
    EMAIL_URL:str = f"https://graph.microsoft.com/v1.0/me/sendMail"
    EMAIL_URL_V2 = lambda sender_email : f"https://graph.microsoft.com/v1.0/users/{sender_email}/sendMail"