
import os
from bs4 import BeautifulSoup
from sharedutils import errlog
from parse import appender 

def main():
    for filename in os.listdir('source'):
        try:
            if filename.startswith('monti-'):
                html_doc='source/'+filename
                file=open(html_doc,'r')
                soup=BeautifulSoup(file,'html.parser')
                divs_name=soup.find_all('a', {"class": "leak-card p-3"})
                for div in divs_name:
                    title = div.find('h5').text.strip()
                    description =  div.find('p').text.strip()
                    appender(title, 'monti', description)
        except:
            errlog('monti: ' + 'parsing fail')
            pass 
                