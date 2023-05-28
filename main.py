"""
CONST = ALL CAPS
variable = variable_name
classes = ClassName
list = name_list
def function = def_name
filename = filename
"""

from classes.info import UserInfo
from classes.play import LoadGooglePage
from classes.clean import CleanHrefs
from classes.parse import ParseUrls
from classes.data import WriteCsv
from classes.color import TherminalColor

# */* test object */*
# from testlist import scraped_url_list


def Getemails(keywords, email):
    user_object = UserInfo(email, keywords)
    print(f'{TherminalColor.HEADER}User: {email} sended keywords: {keywords}{TherminalColor.ENDC} \n\n')
    
    print(f'{TherminalColor.OKCYAN}[Loading] Loading the google page....{TherminalColor.ENDC}')
    playwright_object = LoadGooglePage(keywords)
    print(f'{TherminalColor.OKGREEN}[Info] Google page loaded successfully!{TherminalColor.ENDC}\n')
    
    href_list = playwright_object.Printhrefs()
    print(f'{TherminalColor.OKGREEN}[Info] Found {len(href_list)} hrefs in the google page!{TherminalColor.ENDC}')
    print(f'{TherminalColor.OKCYAN}[Loading] Now going to clean the hrefs from the google page....{TherminalColor.ENDC}\n')
    
    cleaned_object = CleanHrefs(href_list)
    print(f'{TherminalColor.OKGREEN}[Info] Cleaned {len(cleaned_object.cleaned_urls)} links from the google page!{TherminalColor.ENDC}')
    print(f'{TherminalColor.OKCYAN}[Loading] Now going parse emails from the urls....{TherminalColor.ENDC}\n')
    
    parsed_object = ParseUrls(cleaned_object.cleaned_urls)
    print(f'{TherminalColor.OKGREEN}[Info] Parsed {len(parsed_object.website_dicts_list)} urls!{TherminalColor.OKCYAN}')
    
    print(f'{TherminalColor.OKCYAN}[Loading] Going to write to mails.csv...{TherminalColor.OKCYAN}\n')
    WriteCsv(parsed_object.website_dicts_list, keywords)
    print(f'{TherminalColor.OKGREEN}[Info] Succeeded to write to mails.csv!{TherminalColor.OKCYAN}\n\n')
    
    user_object.Addemaillist(parsed_object.website_dicts_list)
    return user_object


keywords_list = []
email = input(f'\n\n{TherminalColor.UNDERLINE}What is your email address?: ')
keywords = 'Not none :)'

while keywords:
    keywords = input('The keywords you want to use (press Enter to start): ')
    if keywords: keywords_list.append(keywords)


print(TherminalColor.ENDC, '\n')

for keywords in keywords_list:
    user_object = Getemails(keywords, email)
    print(f'{TherminalColor.HEADER}[Statistic] Time it Took: {user_object.TimeBetween()} seconds and got {user_object.EMAILLISTLENGTH} contacts for keywords: {user_object.KEYWORDS}{TherminalColor.ENDC}\n\n')


print(f'\n\n{TherminalColor.OKBLUE}All keywords completed! {TherminalColor.ENDC}')

# */* Test results */* 


# Time it Took: 296.6787919998169 cync: Restaurants Purmerend
# Time it Took: 113.61417484283447 cync: Advocaten purmerend

# Time it Took: 162.68579006195068 acync: Restaurants Purmerend
# Time it Took: 13.08481478691101 acync: Advocaten purmerend

# Time it Took: 60.08886671066284 acync and got 111 contacts for keywords: advocaten Amsterdam
