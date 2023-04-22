from bs4 import BeautifulSoup
import requests
import re


class ParseUrls:
    def __init__(self, url_list):
        self.url_list = url_list
        self.USERAGENT_REQUEST = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3', 'Accept-Encoding': 'none', 'Accept-Language': 'en-US,en;q=0.8', 'Connection': 'keep-alive', 'Content-Encoding': 'gzip', 'Content-Type': 'text/html; charset=utf-8'}
        self.first_urls_dicts_list = []
        self.CONTACT_LIST = ['over', 'Over', 'team', 'Team', 'Contact', 'contact']
        
        for url in url_list:
            html_body = self.Makerequest(url)
            emails_set = self.Getemailfromhtml(html_body)
            self.Makedictwebsite(url, emails_set)
            
            
        for dicts in self.first_urls_dicts_list:
            if dicts['level'] != 'none':
                continue
            
            html_body = self.Makerequest(dicts['website'])
            self.Findcontacthref(html_body, url)
            dicts['contacturl'] = self.Findcontacthref(html_body, url)

    def Makeemailfromurl(self, url):
        return

    def Findcontacthref(self, html_body, base_url):
        soup = BeautifulSoup(html_body, 'lxml')
        return next(
            (
                href_link if '.' in href_link else base_url + href_link
                for href_link in soup.find_all('a', href=True)
                if any(x in href_link for x in self.CONTACT_LIST)
            ),
            '',
        )
            
            
    def Makedictwebsite(self, url, emails):
        level = 'sure' if emails else 'none'
        website_dict = {
                'website' : url, 
                'emails' : emails,
                'level' : level, 
                'contacturl' : '',
                
            }
        
        self.first_urls_dicts_list.append(website_dict)
        
        
    def Getemailfromhtml(self, html_body):
        # sourcery skip: inline-immediately-returned-variable
        emails_set = set(re.findall(r'[\w._%+-]+@[A-Za-z.-]+\.[A-Z|a-z]{2,}', html_body, re.I))
        email = {x.lower() for x in emails_set}
        return email
    
    def Makerequest(self, url):
        try:
            return requests.get(url, headers=self.USERAGENT_REQUEST).text
        except requests.exceptions.ConnectionError:
            return ''

    