import os
from bs4 import BeautifulSoup
import json
import html
import re
from sharedutils import errlog
from parse import appender 
import datetime

def main():
    for filename in os.listdir('source'):
        try:
            if filename.startswith('royal-royal4'):
                html_doc='source/'+filename
                file=open(html_doc, 'r')
                soup=BeautifulSoup(file,'html.parser')
                jsonpart = soup.pre.contents
                data = json.loads(jsonpart[0])
                for entry in data['data']:
                    title = html.unescape(entry['title'])
                    website = str(entry['url'])
                    description = html.unescape((re.sub(r'<[^>]*>', '',entry['text'])))
                    date_str = entry['time']
                    dt_object = datetime.datetime.strptime(date_str, "%Y-%B-%d").replace(hour=1, minute=2, second=3, microsecond=456789)
                    published = dt_object.strftime("%Y-%m-%d %H:%M:%S.%f")
                    appender(title, 'royal', description.replace('\n',''),website,published)
                file.close()
        except:
            errlog('royal: ' + 'parsing fail')
            pass    