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

from testlist import hreflist


# def Getemails(keywords, email):
#     UserClass = UserInfo(email, keywords)
#     PlaywrightClass = LoadGooglePage(keywords)
    
#     href_list = PlaywrightClass.Printhrefs()
#     # cleaned_hreflist = CleanHrefs(href_list)
    
#     print(href_list)
    

# Getemails('restaurants purmerend', 'vossjea@gmail.com')


hrefClass = CleanHrefs(hreflist)



