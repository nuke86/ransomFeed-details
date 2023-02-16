
import os
from bs4 import BeautifulSoup
from sharedutils import stdlog, errlog
from parse import appender


def main():
    for filename in os.listdir('source'):
        try:
            if filename.startswith('blackbasta-'):
                html_doc='source/'+filename
                file=open(html_doc,'r')
                soup=BeautifulSoup(file,'html.parser')
                divs_name=soup.find_all('div', {"class": "card"})
                for div in divs_name:
                    title = div.find('a', {"class": "blog_name_link"}).text.strip()
                    descs = div.find_all('p')
                    description = ''
                    for desc in descs:
                        description += desc.text.strip()
                    appender(title, 'blackbasta', description.replace('\n','').replace('ADDRESS',' Address '))
                file.close()
        except:
            errlog('blackbasta: ' + 'parsing fail')
            pass    