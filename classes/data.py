import csv


class WriteCsv:
    '''
    Write email data dicts to mails.csv with with header and footer
    Header includes keywords and rows
    Footer includes credits to Me
    Nothing stored nothing returned
    '''
    def __init__(self, dict_list: list, keywords: str):
        self.dict_list = dict_list
        self.keywords = keywords
        self.FIELDNAMES = ['website', 'emails', 'level', 'contacturl']
        
        self.open_write_csv()
        
    
    def write_csv_header(self, writer: object, f: object) -> None:
        ''' Write csv header with keywords '''
        writer.writerow({'website': 'Keywords used', 'emails': self.keywords})
        writer.writeheader()
        f.write('\n')
        
    
    def write_csv_body(self, writer: object) -> None:   
        ''' Write all the data from the script in the csv file '''        
        for data in self.dict_list:
            email_string = ', '.join(data['emails'])
            data['emails'] = email_string
            writer.writerow(data)
            
    def write_csv_footer(self, writer: object, f: object) -> None:
        ''' Write footer with credits to akula_Arthur '''
        f.write('\n')
        f.write('\n')
        
        writer.writerow({'website': 'automatically generated by OOP mail v2'})
        writer.writerow({'website': 'Made by akula_Arthur'})

    def open_write_csv(self) -> None:
        ''' Open mails.csv and write header, body, and footer data to csv '''
        with open('mails.csv', 'a', encoding='UTF-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.FIELDNAMES)
            
            self.write_csv_header(writer, f)
            self.write_csv_body(writer)
            self.write_csv_footer(writer, f)