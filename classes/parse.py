from bs4 import BeautifulSoup
import httpx
import asyncio
import requests
import re


class ParseUrls:
    '''
    tldr: Get url list and scrape it to get emails
    1. Go to home page and search for emails
    2 . No emails? search for contact url
    3. Go to contact url and search for emails
    4. No emails? Make a email from the given url info@ + url
    End product dicts in list stored in website_dicts_list
    '''
    def __init__(self, url_list: list):
        self.url_list = url_list
        self.USERAGENT_REQUEST = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3', 'Accept-Encoding': 'none', 'Accept-Language': 'en-US,en;q=0.8', 'Connection': 'keep-alive', 'Content-Encoding': 'gzip', 'Content-Type': 'text/html; charset=utf-8'}
        self.website_dicts_list = []
        self.CONTACT_LIST = ['over', 'Over', 'team', 'Team', 'Contact', 'contact']

        # make request for every url in url_list then store it in a list
        url_requests_list = asyncio.run(self.asyncurlrequestsoperator())
        
        # see if request html body contains email if not find Findcontacthref | add to website_dicts_list
        self.Findemailmakedictoperator(url_requests_list)

    	# find every dict who doesnt have a email and has contact url
        # make request to that contact url and store it in contact_url_request_list
        contact_url_list = [dicts for dicts in self.website_dicts_list if dicts['contacturl']]
        contact_url_request_list = asyncio.run(self.asynccontacturlrequestsoperator())
        
        self.Trycontacturltodictoperator(contact_url_list, contact_url_request_list)
        self.Makeurltoemailoperator()

                
                
    async def asynccontacturlrequestsoperator(self) -> list:
        ''' async function that makes requests to all the contact urls '''
        async with httpx.AsyncClient() as client:
            contact_url_request_async_list = [self.Makerequest(dicts['contacturl'], client) for dicts in self.website_dicts_list]
            contact_url_request_list = await asyncio.gather(*contact_url_request_async_list)
        return contact_url_request_list
                
    async def asyncurlrequestsoperator(self) -> list:
        ''' async function that makes requests to all the urls '''
        async with httpx.AsyncClient() as client:
            url_requests_async_list = [self.Makerequest(url, client) for url in self.url_list]
            url_requests_list = await asyncio.gather(*url_requests_async_list)
        return url_requests_list
    
    def Findemailmakedictoperator(self, url_requests_list:list):
        ''' see if request html body contains email if not find Findcontacthref | add to website_dicts_list '''
        for request, url in zip(url_requests_list, self.url_list):
            if emails_set := self.Getemailfromhtml(request):
                self.website_dicts_list.append(self.Makedictwebsite(url, emails_set, ''))
            else:
                contact_url = self.Findcontacthref(request, url)
                self.website_dicts_list.append(self.Makedictwebsite(url, emails_set, contact_url))
    
    def Makeurltoemailoperator(self) -> None:
        ''' for every other link that hasnt gotten a email, make one from url '''
        for dicts in self.website_dicts_list:
            if not dicts['emails']:
                dicts['emails'] = self.Makeemailfromurl(dicts['website'])
                dicts['level'] = 'not sure'

    def Trycontacturltodictoperator(self, contact_url_list:list, contact_url_request_list:list) -> None:
        ''' zip trough contact_url_list, contact_url_request_list and see if contact page contains email, if so add new dict destroy old one '''
        for dicts, request in zip(contact_url_list, contact_url_request_list):
            if emails_set := self.Getemailfromhtml(request):
                self.website_dicts_list.append(self.Makedictwebsite(dicts['website'], emails_set, dicts['contacturl'])) 
                self.website_dicts_list.remove(dicts)


    def Makeemailfromurl(self, url: str) -> set:
        ''' make a email from a url by parsing utrl the do info@ + url '''
        url = url.replace('/', ' ')
        url = url.replace('%', ' ')
        url = next((f'info@{word.capitalize()}' for word in url.split() if '.' in word), url.replace('www.', ' '),)
        return {url}

    def Findcontacthref(self, request: object, base_url: str) -> str:
        '''
        bs4 finds every href tag, if the href tags matches self.CONTACT_LIST then look if the href tag contains a .
        if so return the href else paste the href behind the base_url and return it
        if None match then return emtry string
        '''
        try:
            html_body = request.text
        except Exception:
            return ''

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
            
    def Makedictwebsite(self, website_url: str, emails: set, contact_url: str) -> dict:
        ''' fill in a dict with url information etc. '''
        level = 'sure' if emails else 'none'
        return {
                'website' : website_url, 
                'emails' : emails,
                'level' : level, 
                'contacturl' : contact_url,
            }
        
    def Getemailfromhtml(self, request: object) -> set:
        ''' find a email from the html body and return set '''
        try:
            html_body = request.text
        except Exception:
            html_body = 'https://NONE.com'    

        emails_set = set(re.findall(r'[\w._%+-]+@[A-Za-z.-]+\.[A-Z|a-z]{2,}', html_body, re.I))
        return {x.lower() for x in emails_set}
    
    async def Makerequest(self, url, client) -> object:
        ''' try to make request and get request object, if except return empty string '''
        try:
            return await client.get(url, headers=self.USERAGENT_REQUEST)
        except Exception:
            return ''
