import contextlib
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time
import json


class LoadGooglePage:
    '''
    Load a the google url in Plawright
    Scroll through the bottom of the page
    If the loads takes more then 60 sec then stop Playwright
    If skip end of page list in the html body, then stop Playwright
    End product of all parsed hrefs from the html body stored in ALLHREFS
    '''
    def __init__(self, KEYWORDS: str):
        self.KEYWORDS = KEYWORDS
        self.URL = self.Makeurl()
        self.JSONCOOKIE = self.Loadcookie()
        
        self.USERAGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
        self.SKIPHREFLIST = ['ServiceLogin?', 'products?', 'no_javascript', '/reserve/']
        self.PAGEENDINGSLIST  = ['hebt het einde van de lijst bereikt', 'have reached the end of the list']
    
        self.ALLHREFS = self.Googlepage()
        
    def Printhrefs(self):
        ''' print all hrefs in ALLHREFS '''
        return self.ALLHREFS
    
    def Makeurl(self) -> str:
        ''' Make a google search query link from the keywords'''
        return f"https://www.google.nl/maps/search/{self.KEYWORDS.replace(' ', '+')}"
    
    def Loadcookie(self) -> dict:
        ''' load cookie file to playwright '''
        cookie_file = open('cookie.json')
        return json.load(cookie_file)
    
    def Gethref(self, html_page: str) -> list:
        ''' get all ancher tags and hrefs, then look if href doesnt contain special string in SKIPHREFLIST '''
        soup = BeautifulSoup(html_page, 'lxml')
        hrefItter = (link.get('href') for link in soup.find_all('a') if link.get('href'))
        return (href for href in hrefItter if not any(x for x in self.SKIPHREFLIST if x in href))
    
    def Scrolltohref(self, page: object, href: str) -> None:
        ''' scroll to href into view if needed with playwright '''
        page.wait_for_timeout(1000)
        element = page.locator(f'[href="{href}"]').nth(-1)
        element.scroll_into_view_if_needed()  
        
    def Stopscrolling(self, start_time: float, html_page: str) -> bool:
        ''' stop scrolling if time > 180 seconds or html page includes one of PAGEENDINGSLIST '''
        return any(x in html_page for x in self.PAGEENDINGSLIST) or time.time() - start_time > 60
    
    def Googlepage(self) -> list:
        ''' Load the google page and start scrolling untill th end, then close and get all the hrefs from the html page'''
        allhrefsList = []
        start_time = time.time()
        with sync_playwright() as plays:

            # load user agent and start scrolling
            browser = plays.chromium.launch() #headless=False, slow_mo=50
            context = browser.new_context(user_agent=self.USERAGENT)
            context.add_cookies(self.JSONCOOKIE)

            page = context.new_page()
            page.goto(self.URL)
            page.wait_for_timeout(3000)
            html_page = page.content()

            # with contextlib.suppress(Exception):
            # while not end of page text and not longer then 180 seconds
            while not self.Stopscrolling(start_time, html_page):
                html_page = page.content()
                allhrefsList = list(self.Gethref(html_page))
                last_href = allhrefsList[-1]
                self.Scrolltohref(page, last_href)
            
            return allhrefsList
            
                
                