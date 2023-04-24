from dataclasses import dataclass

@dataclass
class UserInfo:
    '''User data includes email and keywords'''
    USEREMAIL: str
    KEYWORDS: str
    
    def Returnemail(self):
        ''' return User email '''
        return self.USEREMAIL
    
    def Returnkeywords(self):
        ''' return User keywords '''
        return self.KEYWORDS