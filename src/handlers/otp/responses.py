
class Codes:
    
    VERIFIED:str = 'VERIFIED'
    EXPIRED:str = 'EXPIRED'
    INVALID:str = 'INVALID'
    DELIVERED:str = 'DELIVERED'
    NOT_FOUND:str = 'NOT_FOUND'
    TOO_MANY_ATTEMPS:str = 'TOO_MANY_ATTEMPS'
    ALREADY_EXISTS:str = 'ALREADY_EXISTS'
    
class ResponseOtp:
    
    def __init__(self, code:Codes, info = None):
        self.code = code
        self.info = info
