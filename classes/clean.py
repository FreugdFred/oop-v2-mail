import requests


class CleanHrefs:
    def __init__(self, hrefList):
        self.hrefList = hrefList
        self.google_bool = self.Checkifgooglehref()
        
            
        
    def Checkifgooglehref(self):
        # sourcery skip: inline-variable, simplify-numeric-comparison
        # return True if more then 30% are not google links
        nogoogle_amount = sum('www.google' not in href for href in self.hrefList)
        nogoogle_percentage = nogoogle_amount / len(self.hrefList) * 100
        return nogoogle_percentage > 30
    


