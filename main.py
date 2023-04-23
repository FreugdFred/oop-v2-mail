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
from classes.parse import ParseUrls
from classes.data import WriteCsv

# */* test object */*
# from testlist import dict_list


def Getemails(keywords, email):
    UserClass = UserInfo(email, keywords)
    
    print('Loading the google page....')
    PlaywrightClass = LoadGooglePage(keywords)
    print('Google page loaded successfully!')
    
    href_list = PlaywrightClass.Printhrefs()
    print(f'Found {len(href_list)} hrefs in the google page!')
    print('Now going to clean the hrefs from the google page....')
    
    CleanedClass = CleanHrefs(href_list)
    print(f'Cleaned {len(CleanedClass.cleaned_urls)} links from the google page!')
    print('Now going parse emails from the urls....')
    
    """
    Make Parse acync and done!!!!!!!!!!!!!!!
    """
    
    
    
    ParsedClass = ParseUrls(CleanedClass.cleaned_urls)
    print(f'Parsed {len(ParsedClass.website_dicts_list)} urls!')
    
    print('Going to write to mails.csv...')
    WriteCsv(ParsedClass.website_dicts_list, keywords)
    print('Succeeded to write to mails.csv!')
    
    

Getemails('restaurants purmerend', 'vossjea@gmail.com')









