import contextlib
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time
import json


class LoadGooglePage:
    def __init__(self, KEYWORDS):
        self.KEYWORDS = KEYWORDS
        self.URL = self.Makeurl()
        self.JSONCOOKIE = self.Loadcookie()
        
        self.USERAGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
        self.SKIPHREFLIST = ['ServiceLogin?', 'products?', 'no_javascript']
        self.PAGEENDINGSLIST  = ['hebt het einde van de lijst bereikt', 'have reached the end of the list']
    
        self.ALLHREFS = self.Googlepage()
        
    def Printhrefs(self):
        return self.ALLHREFS
    
    def Makeurl(self):
        return f"https://www.google.nl/maps/search/{self.KEYWORDS.replace(' ', '+')}"
    
    def Loadcookie(self):
        cookie_file = open('cookie.json')
        return json.load(cookie_file)
    
    def Gethref(self, html_page):
        # get all ancher tags and hrefs, then look if href doesnt contain special string in SKIPHREFLIST
        soup = BeautifulSoup(html_page, 'lxml')
        hrefItter = (link.get('href') for link in soup.find_all('a') if link.get('href'))
        return (href for href in hrefItter if not any(x for x in self.SKIPHREFLIST if x in href))
    
    def Scrolltohref(self, page, href):
        page.wait_for_timeout(1000)
        element = page.locator(f'[href="{href}"]').nth(-1)
        element.scroll_into_view_if_needed()  
        
    def Stopscrolling(self, start_time, html_page):
        return any(x in html_page for x in self.PAGEENDINGSLIST) or time.time() - start_time > 180
    
    def Googlepage(self):
        start_time = time.time()
        with sync_playwright() as plays:

            browser = plays.chromium.launch(headless=False, slow_mo=50) #headless=False, slow_mo=50
            context = browser.new_context(user_agent=self.USERAGENT)
            context.add_cookies(self.JSONCOOKIE)

            page = context.new_page()
            page.goto(self.URL)
            page.wait_for_timeout(3000)

            # with contextlib.suppress(Exception):
                # while not end of page text and not longer then 180 seconds
                
            while True:
                    html_page = page.content()
                    allhrefsList = list(self.Gethref(html_page))
                    last_href = allhrefsList[-1]
                    
                    self.Scrolltohref(page, last_href)
                    if self.Stopscrolling(start_time, html_page):
                        break
                            
            return allhrefsList
            
                
                