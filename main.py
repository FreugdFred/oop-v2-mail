"""
CONST = ALL CAPS
variable = variable_name
classes = ClassName
list = name_list
def function = Calcname
filename = filename
"""

from classes.info import UserInfo
from classes.play import LoadGooglePage
from classes.clean import CleanHrefs
from classes.parse import ParseUrls
from classes.data import WriteCsv
from classes.color import bcolors

# */* test object */*
# from testlist import scraped_url_list


def Getemails(keywords, email):
    UserClass = UserInfo(email, keywords)
    print(f'{bcolors.HEADER}User: {email} sended keywords: {keywords}{bcolors.ENDC} \n\n')
    
    print(f'{bcolors.OKCYAN}[Loading] Loading the google page....{bcolors.ENDC}')
    PlaywrightClass = LoadGooglePage(keywords)
    print(f'{bcolors.OKGREEN}[Info] Google page loaded successfully!{bcolors.ENDC}\n')
    
    href_list = PlaywrightClass.Printhrefs()
    print(f'{bcolors.OKGREEN}[Info] Found {len(href_list)} hrefs in the google page!{bcolors.ENDC}')
    print(f'{bcolors.OKCYAN}[Loading] Now going to clean the hrefs from the google page....{bcolors.ENDC}\n')
    
    CleanedClass = CleanHrefs(href_list)
    print(f'{bcolors.OKGREEN}[Info] Cleaned {len(CleanedClass.cleaned_urls)} links from the google page!{bcolors.ENDC}')
    print(f'{bcolors.OKCYAN}[Loading] Now going parse emails from the urls....{bcolors.ENDC}\n')
    
    ParsedClass = ParseUrls(CleanedClass.cleaned_urls)
    print(f'{bcolors.OKGREEN}[Info] Parsed {len(ParsedClass.website_dicts_list)} urls!{bcolors.OKCYAN}')
    
    print(f'{bcolors.OKCYAN}[Loading] Going to write to mails.csv...{bcolors.OKCYAN}\n')
    WriteCsv(ParsedClass.website_dicts_list, keywords)
    print(f'{bcolors.OKGREEN}[Info] Succeeded to write to mails.csv!{bcolors.OKCYAN}\n\n')
    
    UserClass.Addemaillist(ParsedClass.website_dicts_list)
    return UserClass


email = input(f'\n\n{bcolors.UNDERLINE}What is your email address?: ')
keywords = input('The keywords you want to use: ')
print(bcolors.ENDC, '\n')

UserClass = Getemails(keywords, email)
print(f'{bcolors.HEADER}[Statistic] Time it Took: {UserClass.TimeBetween()} seconds and got {UserClass.EMAILLISTLENGTH} contacts for keywords: {UserClass.KEYWORDS}{bcolors.ENDC}')


# */* Test results */* 


# Time it Took: 296.6787919998169 cync: Restaurants Purmerend
# Time it Took: 113.61417484283447 cync: Advocaten purmerend

# Time it Took: 162.68579006195068 acync: Restaurants Purmerend
# Time it Took: 13.08481478691101 acync: Advocaten purmerend

# Time it Took: 60.08886671066284 acync and got 111 contacts for keywords: advocaten Amsterdam
