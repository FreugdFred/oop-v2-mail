from bs4 import BeautifulSoup
import requests
import re


class ParseUrls:
    def __init__(self, url_list):
        self.url_list = url_list
        self.USERAGENT_REQUEST = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3', 'Accept-Encoding': 'none', 'Accept-Language': 'en-US,en;q=0.8', 'Connection': 'keep-alive', 'Content-Encoding': 'gzip', 'Content-Type': 'text/html; charset=utf-8'}
        self.website_dicts_list = []
        self.CONTACT_LIST = ['over', 'Over', 'team', 'Team', 'Contact', 'contact']

        # make request for every url in url_list then store it in a list
        url_requests_list = [self.Makerequest(url) for url in self.url_list]
        
        for urls in url_requests_list:
            print(urls)
        
        
        # see if request html body contains email if not find Findcontacthref | add to website_dicts_list
        for request in url_requests_list:
            if emails_set := self.Getemailfromhtml(request):
                self.website_dicts_list.append(self.Makedictwebsite(request.url, emails_set, ''))
            else:
                contact_url = self.Findcontacthref(request, request.url)
                self.website_dicts_list.append(self.Makedictwebsite(request.url, emails_set, contact_url))
                
                

    	# find every dict who doesnt have a email and has contact url
        # make request to that contact url and store it in contact_url_request_list
        contact_url_list = [dicts for dicts in self.website_dicts_list if dicts['contacturl']]
        contact_url_request_list = [self.Makerequest(dicts['contacturl']) for dicts in self.website_dicts_list]
        
        
        # zip trough contact_url_list, contact_url_request_list and see if contact page contains email, if so add new dict destroy cold one
        for dicts, request in zip(contact_url_list, contact_url_request_list):
            if emails_set := self.Getemailfromhtml(request):
                self.website_dicts_list.append(self.Makedictwebsite(dicts['website'], emails_set, request.url)) 
                self.website_dicts_list.remove(dicts)
        
        # for every other link that hasnt gotten a email, make one from url
        for dicts in self.website_dicts_list:
            if not dicts['emails']:
                dicts['emails'] = self.Makeemailfromurl(dicts['website'])
                dicts['level'] = 'not sure'
                

        # # Find every email on the home page and if no email find contact href
        # for url in url_list:
        #     html_body = self.Makerequest(url)
            
        #     if emails_set := self.Getemailfromhtml(html_body):
        #         self.Makedictwebsite(url, emails_set, '')
        #     else:
        #         contact_url = self.Findcontacthref(html_body, url)
        #         self.Makedictwebsite(url, emails_set, contact_url)
                
                
        # if dict has contacturl the make request and scrape the email from the html body
        # for dicts in self.website_dicts_list:
        #     if contact_url := dicts['contacturl']:
        #         html_body = self.Makerequest(contact_url)
        #         dicts['emails'] = self.Getemailfromhtml(html_body)
        #         dicts['level'] = 'sure'




    def Makeemailfromurl(self, url) -> set:
        # make a email from a url by parsing utrl the do info@ + url
        url = url.replace('/', ' ')
        url = url.replace('%', ' ')
        url = url.replace('www.', ' ')
        
        for word in url.split():
            if '.' in word:
                url = f'info@{word.capitalize()}'
                break
        return {url}

    def Findcontacthref(self, request, base_url) -> str:
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
            
    def Makedictwebsite(self, url, emails, contact_url) -> dict:
        # fill in a dict with url information etc.
        level = 'sure' if emails else 'none'
        return {
                'website' : url, 
                'emails' : emails,
                'level' : level, 
                'contacturl' : contact_url,
            }
        
        
    def Getemailfromhtml(self, html_body) -> set:
        # find a email from the html body and return set
        emails_set = set(re.findall(r'[\w._%+-]+@[A-Za-z.-]+\.[A-Z|a-z]{2,}', html_body, re.I))
        return {x.lower() for x in emails_set}
    
    def Makerequest(self, url) -> str:
        # try to make request and get html body, if except return emty string
        try:
            return requests.get(url, headers=self.USERAGENT_REQUEST)
        except Exception:
            return ''

    