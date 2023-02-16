import os
import re
from bs4 import BeautifulSoup
from sharedutils import errlog
from parse import appender
import json

def main():
    for filename in os.listdir('source'):
        try:
            if filename.startswith('ransomhouse-zoh'):
                html_doc='source/'+filename
                file=open(html_doc, 'r')
                soup=BeautifulSoup(file,'html.parser')
                jsonpart= soup.pre.contents # type: ignore
                data = json.loads(jsonpart[0]) # type: ignore
                for element in data['data']:
                    title = element['header']
                    website = element['url']
                    description = re.sub(r'<[^>]*>', '',element['info'])
                    # stdlog(title)
                    appender(title, 'ransomhouse', description,website)
                file.close()
        except:
            errlog('ransomhouse: ' + 'parsing fail')
            pass