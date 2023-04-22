import requests
from bs4 import BeautifulSoup
import re
import time

class CleanHrefs:
    def __init__(self, hrefList):
        self.hrefList = hrefList
        self.google_bool = self.Checkifgooglehref()
        
        self.HTTPLIST = ['https://', 'http://']
        self.SKIP_URL_LIST = ['google', '.png', 'gstatic', 'broofa.com', 'ggpht.', 'schema.org', 'w3.org']
        self.SKIPHREF_LIST = ['ServiceLogin?', 'products?', 'no_javascript', '/reserve/']
        self.USERAGENT_REQUEST = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3', 'Accept-Encoding': 'none', 'Accept-Language': 'en-US,en;q=0.8', 'Connection': 'keep-alive', 'Content-Encoding': 'gzip', 'Content-Type': 'text/html; charset=utf-8'}
        self.GOOGLE_COOKIE_REQUEST = {'CONSENT' : 'YES+'}
          
          
        if not self.google_bool:
            for href in self.hrefList:
                print(self.geturlfromplace(href))
                time.sleep(1)
                
            
    # def Geturlfromplace(self, html_page) -> list:
    #     # get all ancher tags and hrefs, then look if href doesnt contain special string in SKIPHREF_LIST
    #     soup = BeautifulSoup(html_page, 'lxml')
    #     hrefItter = (link.get('href') for link in soup.find_all('a') if link.get('href'))
    #     return (href for href in hrefItter if not any(x for x in self.SKIPHREF_LIST if x in href))
        
    def Checkifgooglehref(self) -> bool:
        # sourcery skip: inline-variable, simplify-numeric-comparison
        # return True if more then 30% are not google links
        nogoogle_amount = sum('www.google' not in href for href in self.hrefList)
        nogoogle_percentage = nogoogle_amount / len(self.hrefList) * 100
        return nogoogle_percentage > 30
    
    # def geturlfromplace(self, href) -> str or None:
    #     html_request_body = requests.get(href, headers=self.USERAGENT_REQUEST, cookies=self.GOOGLE_COOKIE_REQUEST).text

    #     soup = BeautifulSoup(html_request_body, 'lxml')
    #     hrefItter = (link.get('href') for link in soup.find_all('a') if link.get('href'))
    #     allhrefs = (href for href in hrefItter if not any(x for x in self.SKIPHREF_LIST if x in href))

    #     for href in hrefItter:
    #         print(f'href: {href}')

    #     return next((href_page for href_page in allhrefs if all(x not in href_page for x in self.SKIP_URL_LIST) and any(x in href_page for x in self.HTTPLIST)), None)
    
    
    def geturlfromplace(self, href) -> str or None:
        html_request_body = requests.get(href, headers=self.USERAGENT_REQUEST, cookies=self.GOOGLE_COOKIE_REQUEST).text

        soup = BeautifulSoup(html_request_body, 'lxml')

        href_tags = soup.find_all(href=True)
        for href in href_tags:
            print("Found the URL:", href['href'])
            
        return None

