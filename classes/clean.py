from urllib.parse import urlparse
import requests
import re
import time


class CleanHrefs:
    '''
    Look if email list contains to much google links, if to much google links then scrape website url from the google/place
    and put it in the list, delete the non google urls
    if not to much google urls, then delete google urls
    End product stored in cleaned_urls
    '''
    def __init__(self, hrefList: list):
        self.hrefList = list(filter(lambda item: item is not None, hrefList))
        self.google_bool = self.check_amount_google_hrefs()
        
        self.HTTPLIST = ['https://', 'http://']
        self.SKIP_URL_LIST = ['google', '.png', 'gstatic', 'broofa.com', 'ggpht.', 'schema.org', 'w3.org', 'https://g.page/']
        self.SKIPHREF_LIST = ['ServiceLogin?', 'products?', 'no_javascript', '/reserve/']
        self.USERAGENT_REQUEST = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3', 'Accept-Encoding': 'none', 'Accept-Language': 'en-US,en;q=0.8', 'Connection': 'keep-alive', 'Content-Encoding': 'gzip', 'Content-Type': 'text/html; charset=utf-8'}
        self.GOOGLE_COOKIE_REQUEST = {'CONSENT' : 'YES+'}
        
        # if more then 30% url are not from google then remove_google_emails() else get_url_from_google_place()
        if self.google_bool:
            self.cleaned_urls = [self.remove_google_emails(href) for href in self.hrefList]
        else:
            non_google_url_list = [self.remove_non_google_emails(href) for href in self.hrefList]
            self.cleaned_urls = [self.get_url_from_google_place(href) for href in non_google_url_list]
            
        # remove all none values for list
        self.cleaned_urls = list(filter(lambda item: item is not None, self.cleaned_urls))
        
    
    def remove_non_google_emails(self, url:str) -> str or None:
        ''' if google not in url the return None else return url '''
        return url if 'google' in url else None
                
    def remove_google_emails(self, url:str) -> str or None:
        ''' return url if url does not conatin componemnts of SKIP_URL_LIST '''
        return url if all(x not in url for x in self.SKIP_URL_LIST) else None
        
    def check_amount_google_hrefs(self) -> bool:
        ''' return True if more then 30% are not google links '''
        # sourcery skip: inline-variable, simplify-numeric-comparison
        nogoogle_amount = sum('www.google' not in href for href in self.hrefList)
        nogoogle_percentage = nogoogle_amount / len(self.hrefList) * 100
        return nogoogle_percentage > 30
    
    def get_url_from_google_place(self, href:str) -> str or None:
        ''' Fetch website url from google place html body '''
        try:
            html_request_body = requests.get(href, headers=self.USERAGENT_REQUEST, cookies=self.GOOGLE_COOKIE_REQUEST).text
        except Exception:
            return None

        # dont let google block us :)
        time.sleep(0.5)

        for lines in re.split(r'"|\\', html_request_body):
            # if line contains SKIP_URL_LIST components or does not contain HTTPLIST then go trough next loop
            if all(x not in lines for x in self.HTTPLIST) or any(x in lines for x in self.SKIP_URL_LIST):
                continue

            if 'u003d' in lines:
                parsed_url =  lines.replace('u003d', '')
                return f"http://{urlparse(parsed_url).netloc}"

        return None

