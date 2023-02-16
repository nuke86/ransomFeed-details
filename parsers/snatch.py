import os
from bs4 import BeautifulSoup
from sharedutils import errlog
from parse import appender

def main():
    for filename in os.listdir('source'):
        try:
            if filename.startswith('snatch-'):
                html_doc='source/'+filename
                file=open(html_doc,'r')
                soup=BeautifulSoup(file,'html.parser')
                divs_name=soup.find_all('div', {"class": "ann-block"})
                for div in divs_name:
                    title = div.find('div', {'class': 'a-b-n-name'}).text.strip()
                    description = div.find('div', {'class': 'a-b-text'}).text.strip()
                    appender(title, 'snatch', description)
                file.close()
        except:
            errlog('snatch: ' + 'parsing fail')
            pass