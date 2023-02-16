import os
from bs4 import BeautifulSoup
from sharedutils import errlog
import parse

def main():
    for filename in os.listdir('source'):
        try:
            if filename.startswith('lockbit3-'):
                html_doc='source/'+filename
                file=open(html_doc,'r')
                soup=BeautifulSoup(file,'html.parser')
                divs_name=soup.find_all('div', {"class": "post-block bad"})
                for div in divs_name:
                    title = div.find('div',{"class": "post-title"}).text.strip()
                    description = div.find('div',{"class" : "post-block-text"}).text.strip()
                    parse.appender(title, 'lockbit3', description.replace('\n',''))
                divs_name=soup.find_all('div', {"class": "post-block good"})
                for div in divs_name:
                    title = div.find('div',{"class": "post-title"}).text.strip()
                    description = div.find('div',{"class" : "post-block-text"}).text.strip()
                    parse.appender(title, 'lockbit3', description.replace('\n',''))
                file.close()
        except:
            errlog('lockbit3: ' + 'parsing fail')
            pass    