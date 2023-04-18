"""
CONST = ALL CAPS
variable = variable_name
classes = ClassName
list = listName
def function = Calcname
filename = filename
"""

from classes.info import UserInfo
from classes.play import LoadGooglePage
from classes.clean import CleanHrefs


def Getemails(keywords, email):
    UserClass = UserInfo(email, keywords)
    PlaywrightClass = LoadGooglePage(keywords)
    
    href_list = PlaywrightClass.Printhrefs()
    cleaned_hreflist = CleanHrefs(href_list)
    
    
    for cleaned in cleaned_hreflist:
        print(cleaned)



    
Getemails('advocaten Amsterdam', 'vossjea@gmail.com')