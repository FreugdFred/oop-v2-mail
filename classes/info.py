from dataclasses import dataclass

@dataclass
class UserInfo:
    USEREMAIL: str
    KEYWORDS: str
    
    def Returnemail(self):
        return self.USEREMAIL
    
    def Returnkeywords(self):
        return self.KEYWORDS