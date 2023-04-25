from dataclasses import dataclass, field
import time


@dataclass
class UserInfo:
    '''User data includes email and keywords'''
    USEREMAIL: str
    KEYWORDS: str
    EMAILLIST: list = field(default_factory=list) 
    EMAILLISTLENGTH: int = 0
    STARTTIME: float = time.time()
    
    def Returnemail(self):
        ''' return User email '''
        return self.USEREMAIL
    
    def Returnkeywords(self):
        ''' return User keywords '''
        return self.KEYWORDS
    
    def Addemaillist(self, EMAILLIST):
        ''' Add emaillist to dataclass, and add length to class '''
        self.EMAILLIST = EMAILLIST
        self.EMAILLISTLENGTH = len(EMAILLIST)
        
    def TimeBetween(self):
        ''' Measure time between time first initiated to when called '''
        return time.time() - self.STARTTIME
        
        
    