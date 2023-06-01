from bs4 import BeautifulSoup
import httpx
import asyncio
import requests
import re


class ParseUrls:
    '''
    tldr: Get url list and scrape it to get emails
    1. Go to home page and search for emails
    2. No emails? search for contact url
    3. Go to contact url and search for emails
    4. No emails? Make a email from the given url info@ + url
    End product dicts in list stored in website_dicts_list
    '''
    def __init__(self, url_list: list):
        self.url_list = [self.make_url_dict(url) for url in url_list]
        self.USERAGENT_REQUEST = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3', 'Accept-Encoding': 'none', 'Accept-Language': 'en-US,en;q=0.8', 'Connection': 'keep-alive', 'Content-Encoding': 'gzip', 'Content-Type': 'text/html; charset=utf-8'}
        self.CONTACT_LIST = ['over', 'Over', 'team', 'Team', 'Contact', 'contact']
        
        # async request for all the urls
        self.url_list = asyncio.run(self.ansync_request_operator(True))
        
        
        # loops trough dicts and tries to get email and phonenumber, if no email? then find contact_href, no contact_href? then make email out of the url
        for dicts in self.url_list:
            dicts['emails'] = self.find_email_from_html_body(dicts['requestobject'])
            dicts['phonenumbers'] = self.find_phonenumber_from_html_body(dicts['requestobject'])
            
            if not dicts['emails']:
                dicts['contacturl'] = self.find_contact_href(dicts['requestobject'], dicts['website'])
                
                if not dicts['contacturl']:
                    dicts['emails'] = self.make_email_from_url(dicts['website'])
                    dicts['level'] = 'not sure'
                

        # async request for all the contact urls
        self.url_list = asyncio.run(self.ansync_request_operator(False))
        
        # loops trough dicts and tries to get email and phonenumber, no contact_href? then make email out of the url
        for dicts in self.url_list:
            dicts['emails'] = self.find_email_from_html_body(dicts['requestobject'])
            dicts['phonenumbers'] = self.find_phonenumber_from_html_body(dicts['requestobject'])
            
            if not dicts['emails']:
                dicts['emails'] = self.make_email_from_url(dicts['website'])
                dicts['level'] = 'not sure'
                
        # removes reqquest object from dicts
        for dicts in self.url_list:
            dicts.pop('requestobject')
        

    async def async_request_maker(self, url_dict:dict, client: object, round_operator:bool) -> dict:
        ''' try to make request and get request object, if except return empty string '''
        url_keyword = 'website' if round_operator else 'contacturl'
        try:
            req = await client.get(url_dict[url_keyword], headers=self.USERAGENT_REQUEST)
            
            if req.status_code == 301:
                url_dict[url_keyword] = url_dict[url_keyword].replace('http://', 'https://')
                
            req = await client.get(url_dict[url_keyword], headers=self.USERAGENT_REQUEST)
            
            url_dict['requestobject'] = req
            return await url_dict
        
        except Exception:
            return url_dict
        
    async def ansync_request_operator(self, contact_bool: bool) -> list:
        async with httpx.AsyncClient() as client:
            url_requests_async_list = [self.async_request_maker(url_dict, client, contact_bool) for url_dict in self.url_list]
            request_objects_list = await asyncio.gather(*url_requests_async_list)
        return request_objects_list
    
    def make_url_dict(self, website_url: str) -> dict:
        ''' fill in a dict with url information etc. '''
        return {
                'website' : website_url, 
                'emails' : None,
                'phonenumbers': None,
                'level' : 'sure',
                'requestobject' : None,
                'contacturl' : None,
            }

    def make_email_from_url(self, url: str) -> set:
        ''' make a email from a url by parsing utrl the do info@ + url '''
        url = url.lower()
        url = url.replace('/', ' ')
        url = url.replace('%', ' ')
        url = next((f'info@{word.capitalize()}' for word in url.split() if '.' in word), url.replace('www.', ' '),)
        return {url}

    def find_contact_href(self, request: object, base_url: str) -> str:
        '''
        bs4 finds every href tag, if the href tags matches self.CONTACT_LIST then look if the href tag contains a .
        if so return the href else paste the href behind the base_url and return it
        if None match then return emtry string
        '''
        try:
            html_body = request.text
        except Exception:
            return None


        soup = BeautifulSoup(html_body, 'lxml')
        
        return next(
            (
                href_link['href']
                if '.' in href_link['href']
                else base_url + href_link['href']
                for href_link in soup.find_all('a', href=True)
                if any(x in href_link['href'] for x in self.CONTACT_LIST)
            ),
            '',
        )

        
    def find_email_from_html_body(self, request: object) -> set:
        ''' find a email from the html body and return set '''
        try:
            html_body = request.text
        except Exception:
            return set()

        emails_set = set(re.findall(r'[\w._%+-]+@[A-Za-z.-]+\.[A-Z|a-z]{2,}', html_body, re.I))
        return {x.lower() for x in emails_set}
    
    def find_phonenumber_from_html_body(self, request: object) -> set:
        ''' find a phonenumber from the html body and return set '''
        try:
            html_body = request.text
        except Exception:
            return set()


        phone_set = re.findall(r'(?:^|\s)(((?:\+|0{2})(?:49|43|33)[-\. ]?|0)([1-9]\d{1,2}[-\. ]?|\([1-9]\d{1,2}\)[-\. ]?)(\d{6,9}|\d{2,3}[-\. ]\d{4,6}))', html_body, re.I)
        phone_list = flatten_list(list(phone_set))
        return {phonenumber for phonenumber in phone_list if len(phonenumber) > 9}

        
        
def flatten_list(l):
    ''' Makes one list from a list in a list'''
    return [item for sublist in l for item in sublist]