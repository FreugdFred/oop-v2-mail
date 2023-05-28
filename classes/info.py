from dataclasses import dataclass, field
from math import floor
import time


@dataclass
class UserInfo:
    '''User data includes email and keywords'''
    IDCSV: str
    USEREMAIL: str
    KEYWORDS: str
    EMAILLIST: list = field(default_factory=list) 
    EMAILLISTLENGTH: int = 0
    STARTTIME: float = time.time()
    
    def return_email(self):
        ''' return User email '''
        return self.USEREMAIL
    
    def return_keywords(self):
        ''' return User keywords '''
        return self.KEYWORDS
    
    def add_email_list(self, EMAILLIST):
        ''' Add emaillist to dataclass, and add length to class '''
        self.EMAILLIST = EMAILLIST
        self.EMAILLISTLENGTH = len(EMAILLIST)
        
    def time_between(self):
        ''' Measure time between time first initiated to when called '''
        return floor(time.time() - self.STARTTIME)