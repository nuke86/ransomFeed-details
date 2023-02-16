import os
from bs4 import BeautifulSoup
from sharedutils import errlog
from parse import appender

def main():
    for filename in os.listdir('source'):
        try:
            if filename.startswith('mallox-'):
                html_doc='source/'+filename
                file=open(html_doc,'r')
                soup=BeautifulSoup(file,'html.parser')
                divs_name=soup.find_all('div', {"class": "card mb-4 box-shadow"})
                for div in divs_name:
                    title = div.find('h5',{"class": "card-title"}).text.strip()
                    description = ''
                    for p in div.find_all('p'):
                        description+=p.text + ' '
                    appender(title, 'mallox', description)
                file.close()
        except:
            errlog('mallox: ' + 'parsing fail')
            pass