from abc import ABC, abstractmethod

class BaseEvent(ABC):
    @property
    def TEMPLATE(self):
        raise NotImplementedError
    
    @property
    def SUBJECT(self):
        raise NotImplementedError
    
    @property
    def TYPE(self):
        raise NotImplementedError
    
    @property
    def TO(self):
        raise NotImplementedError
    
    @property
    def DATA(self):
        raise NotImplementedError

   
