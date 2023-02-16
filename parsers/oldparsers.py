import os
import json
from sys import platform
from datetime import datetime
from sharedutils import runshellcmd
# from sharedutils import todiscord, totwitter, toteams
from sharedutils import stdlog, errlog   # , honk
from parse import appender

# on macOS we use 'grep -oE' over 'grep -oP'
if platform == 'darwin':
    fancygrep = 'ggrep -oP'
else:
    fancygrep = 'grep -oP'

'''
all parsers here are shell - mix of grep/sed/awk & perl - runshellcmd is a wrapper for subprocess.run
'''

def synack():
    stdlog('parser: ' + 'synack')
    parser='''
    grep 'card-title' source/synack-*.html --no-filename | cut -d ">" -f2 | cut -d "<" -f1
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('synack: ' + 'parsing fail')
    for post in posts:
        appender(post, 'synack')

def everest():
    stdlog('parser: ' + 'everest')
    parser = '''
    grep '<h2 class="entry-title' source/everest-*.html | cut -d '>' -f3 | cut -d '<' -f1
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('everest: ' + 'parsing fail')
    for post in posts:
        appender(post, 'everest')


def suncrypt():
    stdlog('parser: ' + 'suncrypt')
    parser = '''
    cat source/suncrypt-*.html | tr '>' '\n' | grep -A1 '<a href="client?id=' | sed -e '/^--/d' -e '/^<a/d' | cut -d '<' -f1 | sed -e 's/[ \t]*$//' "$@" -e '/Read more/d'
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('suncrypt: ' + 'parsing fail')
    for post in posts:
        appender(post, 'suncrypt')

def lorenz():
    stdlog('parser: ' + 'lorenz')
    parser = '''
    grep 'h3' source/lorenz-*.html --no-filename | cut -d ">" -f2 | cut -d "<" -f1 | sed -e 's/^ *//g' -e '/^$/d' -e 's/[[:space:]]*$//'
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('lorenz: ' + 'parsing fail')
    for post in posts:
        appender(post, 'lorenz')

def lockbit2():
    stdlog('parser: ' + 'lockbit2')
    # egrep -h -A1 'class="post-title"' source/lockbit2-* | grep -v 'class="post-title"' | grep -v '\--' | cut -d'<' -f1 | tr -d ' '
    parser = '''
    awk -v lines=2 '/post-title-block/ {for(i=lines;i;--i)getline; print $0 }' source/lockbit2-*.html | cut -d '<' -f1 | sed -e 's/^ *//g' -e 's/[[:space:]]*$//' | sort | uniq
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('lockbit2: ' + 'parsing fail')
    for post in posts:
        appender(post, 'lockbit2')


def arvinclub():
    stdlog('parser: ' + 'arvinclub')
    # grep 'bookmark' source/arvinclub-*.html --no-filename | cut -d ">" -f3 | cut -d "<" -f1
    parser = '''
    grep 'rel="bookmark">' source/arvinclub-*.html -C 1 | grep '</a>' | sed 's/^[^[:alnum:]]*//' | cut -d '<' -f 1 | sed -e 's/^ *//g' -e 's/[[:space:]]*$//'
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('arvinclub: ' + 'parsing fail')
    for post in posts:
        appender(post, 'arvinclub')

def avaddon():
    stdlog('parser: ' + 'avaddon')
    parser = '''
    grep 'h6' source/avaddon-*.html --no-filename | cut -d ">" -f3 | sed -e s/'<\/a'//
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('avaddon: ' + 'parsing fail')
    for post in posts:
        appender(post, 'avaddon')

def xinglocker():
    stdlog('parser: ' + 'xinglocker')
    parser = '''
    grep "h3" -A1 source/xinglocker-*.html --no-filename | grep -v h3 | awk -v n=4 'NR%n==1' | sed -e 's/^[ \t]*//' -e 's/^ *//g' -e 's/[[:space:]]*$//'
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('xinglocker: ' + 'parsing fail')
    for post in posts:
        appender(post, 'xinglocker')
    
def ragnarlocker():
    stdlog('parser: ' + 'ragnarlocker')
    json_parser = '''
    grep 'var post_links' source/ragnarlocker-*.html --no-filename | sed -e s/"        var post_links = "// -e "s/ ;//"
    '''
    posts = runshellcmd(json_parser)
    post_json = json.loads(posts[0])
    with open('source/ragnarlocker.json', 'w', encoding='utf-8') as f:
        json.dump(post_json, f, indent=4)
        f.close()
    if len(post_json) == 1:
        errlog('ragnarlocker: ' + 'parsing fail')
    for post in post_json:
        try:
            appender(post['title'], 'ragnarlocker')
        except TypeError:
            errlog('ragnarlocker: ' + 'parsing fail')

def revil():
    stdlog('parser: ' + 'revil')
    # grep 'href="/posts' source/revil-*.html --no-filename | cut -d '>' -f2 | sed -e s/'<\/a'// -e 's/^[ \t]*//'
    parser = '''
    grep 'justify-content-between' source/revil-*.html --no-filename | cut -d '>' -f 3 | cut -d '<' -f 1 | sed -e 's/^ *//g' -e 's/[[:space:]]*$//' -e '/ediban/d'
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('revil: ' + 'parsing fail')
    for post in posts:
        appender(post, 'revil')

def conti():
    stdlog('parser: ' + 'conti')
    # grep 'class="title">&' source/conti-*.html --no-filename | cut -d ";" -f2 | sed -e s/"&rdquo"//
    parser = '''
    grep 'newsList' source/conti-continewsnv5ot*.html --no-filename | sed -e 's/        newsList(//g' -e 's/);//g' | jq '.[].title' -r  || true
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('conti: ' + 'parsing fail')
    for post in posts:
        appender(post, 'conti')
    
def pysa():
    stdlog('parser: ' + 'pysa')
    parser = '''
    grep 'icon-chevron-right' source/pysa-*.html --no-filename | cut -d '>' -f3 | sed 's/^ *//g'
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('pysa: ' + 'parsing fail')
    for post in posts:
        appender(post, 'pysa')

def nefilim():
    stdlog('parser: ' + 'nefilim')
    parser = '''
    grep 'h2' source/nefilim-*.html --no-filename | cut -d '>' -f3 | sed -e s/'<\/a'//
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('nefilim: ' + 'parsing fail')
    for post in posts:
        appender(post, 'nefilim') 

def mountlocker():
    stdlog('parser: ' + 'mountlocker')
    parser = '''
    grep '<h3><a href=' source/mount-locker-*.html --no-filename | cut -d '>' -f5 | sed -e s/'<\/a'// -e 's/^ *//g' -e 's/[[:space:]]*$//'
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('mountlocker: ' + 'parsing fail')
    for post in posts:
        appender(post, 'mountlocker')

def babuk():
    stdlog('parser: ' + 'babuk')
    parser = '''
    grep '<h5>' source/babuk-*.html --no-filename | sed 's/^ *//g' | cut -d '>' -f2 | cut -d '<' -f1 | grep -wv 'Hospitals\|Non-Profit\|Schools\|Small Business' | sed '/^[[:space:]]*$/d'
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('babuk: ' + 'parsing fail')
    for post in posts:
        appender(post, 'babuk')
    
def ransomexx():
    stdlog('parser: ' + 'ransomexx')
    parser = '''
    grep 'card-title' source/ransomexx-*.html --no-filename | cut -d '>' -f2 | sed -e s/'<\/h5'// -e 's/^ *//g' -e 's/[[:space:]]*$//'
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('ransomexx: ' + 'parsing fail')
    for post in posts:
        appender(post, 'ransomexx')

#def cuba():
#    stdlog('parser: ' + 'cuba')
#    # grep '<p>' source/cuba-*.html --no-filename | cut -d '>' -f3 | cut -d '<' -f1
#    # grep '<a href="http://' source/cuba-cuba4i* | cut -d '/' -f 4 | sort -u
#    parser = '''
#    grep --no-filename '<a href="/company/' source/cuba-*.html | cut -d '/' -f 3 | cut -d '"' -f 1 | sort --uniq | grep -v company
#    '''
#    posts = runshellcmd(parser)
#    if len(posts) == 1:
#        errlog('cuba: ' + 'parsing fail')
#    for post in posts:
#        appender(post, 'cuba')

def pay2key():
    stdlog('parser: ' + 'pay2key')
    parser = '''
    grep 'h3><a href' source/pay2key-*.html --no-filename | cut -d '>' -f3 | sed -e s/'<\/a'//
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('pay2key: ' + 'parsing fail')
    for post in posts:
        appender(post, 'pay2key')

def azroteam():
    stdlog('parser: ' + 'azroteam')
    parser = '''
    grep "h3" -A1 source/aztroteam-*.html --no-filename | grep -v h3 | awk -v n=4 'NR%n==1' | sed -e 's/^[ \t]*//'
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('azroteam: ' + 'parsing fail')
    for post in posts:
        appender(post, 'azroteam')

def lockdata():
    stdlog('parser: ' + 'lockdata')
    parser = '''
    grep '<a href="/view.php?' source/lockdata-*.html --no-filename | cut -d '>' -f2 | cut -d '<' -f1
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('lockdata: ' + 'parsing fail')
    for post in posts:
        appender(post, 'lockdata')
    
def blacktor():
    stdlog('parser: ' + 'blacktor')
    # sed -n '/tr/{n;p;}' source/bl@cktor-*.html | grep 'td' | cut -d '>' -f2 | cut -d '<' -f1
    parser = '''
    grep '>Details</a></td>' source/blacktor-*.html --no-filename | cut -f2 -d '"' | cut -f 2- -d- | cut -f 1 -d .
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('blacktor: ' + 'parsing fail')
    for post in posts:
        appender(post, 'blacktor')
    
def darkleakmarket():
    stdlog('parser: ' + 'darkleakmarket')
    parser = '''
    grep 'page.php' source/darkleakmarket-*.html --no-filename | sed -e 's/^[ \t]*//' | cut -d '>' -f3 | sed '/^</d' | cut -d '<' -f1 | sed -e 's/^ *//g' -e 's/[[:space:]]*$//'
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('darkleakmarket: ' + 'parsing fail')
    for post in posts:
        appender(post, 'darkleakmarket')

def blackmatter():
    stdlog('parser: ' + 'blackmatter')
    parser = '''
    grep '<h4 class="post-announce-name" title="' source/blackmatter-*.html --no-filename | cut -d '"' -f4 | sort -u
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('blackmatter: ' + 'parsing fail')
    for post in posts:
        appender(post, 'blackmatter')

def payloadbin():
    stdlog('parser: ' + 'payloadbin')
    parser = '''
    grep '<h4 class="h4' source/payloadbin-*.html --no-filename | cut -d '>' -f3 | cut -d '<' -f 1
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('payloadbin: ' + 'parsing fail')
    for post in posts:
        appender(post, 'payloadbin')

def groove():
    stdlog('parser: ' + 'groove')
    parser = '''
    egrep -o 'class="title">([[:alnum:]]| |\.)+</a>' source/groove-*.html | cut -d '>' -f2 | cut -d '<' -f 1
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('groove: ' + 'parsing fail')
    for post in posts:
        appender(post, 'groove')

def bonacigroup():
    stdlog('parser: ' + 'bonacigroup')
    parser = '''
    grep 'h5' source/bonacigroup-*.html --no-filename | cut -d '>' -f 3 | cut -d '<' -f 1
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('bonacigroup: ' + 'parsing fail')
    for post in posts:
        appender(post, 'bonacigroup')

def karma():
    stdlog('parser: ' + 'karma')
    parser = '''
    grep "h2" source/karma-*.html --no-filename | cut -d '>' -f 3 | cut -d '<' -f 1 | sed '/^$/d'
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('karma: ' + 'parsing fail')
    for post in posts:
        appender(post, 'karma')


def spook():
    stdlog('parser: ' + 'spook')
    parser = '''
    grep 'h2 class' source/spook-*.html --no-filename | cut -d '>' -f 3 | cut -d '<' -f 1 | sed -e 's/^ *//g' -e '/^$/d'
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('spook: ' + 'parsing fail')
    for post in posts:
        appender(post, 'spook')

def quantum():
    stdlog('parser: ' + 'quantum')
    parser = '''
    awk '/h2/{getline; print}' source/quantum-*.html | sed -e 's/^ *//g' -e '/<\/a>/d'
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('quantum: ' + 'parsing fail')
    for post in posts:
        appender(post, 'quantum')

def atomsilo():
    stdlog('parser: ' + 'atomsilo')
    parser = '''
    grep "h4" source/atomsilo-*.html | cut -d '>' -f 3 | cut -d '<' -f 1 | sed -e 's/^ *//g' -e 's/[[:space:]]*$//'
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('atomsilo: ' + 'parsing fail')
    for post in posts:
        appender(post, 'atomsilo')
        
def lv():
    stdlog('parser: ' + 'lv')
    # %s "blog-post-title.*?</a>" source/lv-rbvuetun*.html | cut -d '>' -f 3 | cut -d '<' -f 1
    parser = '''
    jq -r '.posts[].title' source/lv-rbvuetun*.html | sed -e 's/^ *//g' -e 's/[[:space:]]*$//'
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('lv: ' + 'parsing fail')
    for post in posts:
        appender(post, 'lv')

def five4bb47h():
    stdlog('parser: ' + 'sabbath')
    parser = '''
    %s "aria-label.*?>" source/sabbath-*.html | cut -d '"' -f 2 | sed -e '/Search button/d' -e '/Off Canvas Menu/d' -e '/Close drawer/d' -e '/Close search modal/d' -e '/Header Menu/d' | tr "..." ' ' | grep "\S" | cat
    ''' % (fancygrep)
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('sabbath: ' + 'parsing fail')
    for post in posts:
        appender(post, 'sabbath')

def midas():
    stdlog('parser: ' + 'midas')
    parser = '''
    grep "/h3" source/midas-*.html --no-filename | sed -e 's/<\/h3>//' -e 's/^ *//g' -e '/^$/d' -e 's/^ *//g' -e 's/[[:space:]]*$//' -e '/^$/d'
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('midas: ' + 'parsing fail')
    for post in posts:
        appender(post, 'midas')

#def snatch():
#    stdlog('parser: ' + 'snatch')
#    parser = '''
#    %s "a-b-n-name.*?</div>" source/snatch-*.html | cut -d '>' -f 2 | cut -d '<' -f 1
#    ''' % (fancygrep)
#    posts = runshellcmd(parser)
#    if len(posts) == 1:
#        errlog('snatch: ' + 'parsing fail')
#    for post in posts:
#        appender(post, 'snatch')

def marketo():
    stdlog('parser: ' + 'marketo')
    parser = '''
    grep '<a href="/lot' source/marketo-*.html | sed -e 's/^ *//g' -e '/Show more/d' -e 's/<strong>//g' | cut -d '>' -f 2 | cut -d '<' -f 1 | sed -e '/^$/d'
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('marketo: ' + 'parsing fail')
    for post in posts:
        appender(post, 'marketo')

def rook():
    stdlog('parser: ' + 'rook')
    parser = '''
    grep 'class="post-title"' source/rook-*.html | cut -d '>' -f 2 | cut -d '<' -f 1 | sed '/^&#34/d'
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('rook: ' + 'parsing fail')
    for post in posts:
        appender(post, 'rook')

def cryp70n1c0d3():
    stdlog('parser: ' + 'cryp70n1c0d3')
    parser = '''
    grep '<td class="selection"' source/cryp70n1c0d3-*.html | cut -d '>' -f 2 | cut -d '<' -f 1 | sed -e 's/^ *//g' -e 's/[[:space:]]*$//'
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('cryp70n1c0d3: ' + 'parsing fail')
    for post in posts:
        appender(post, 'cryp70n1c0d3')

def mosesstaff():
    stdlog('parser: ' + 'mosesstaff')
    parser = '''
    grep '<h2 class="entry-title">' source/moses-moses-staff.html -A 3 --no-filename | grep '</a>' | sed 's/^ *//g' | cut -d '<' -f 1 | sed 's/[[:space:]]*$//'
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('mosesstaff: ' + 'parsing fail')
    for post in posts:
        appender(post, 'mosesstaff')

def nightsky():
    stdlog('parser: ' + 'nightsky')
    parser = '''
    grep 'class="mdui-card-primary-title"' source/nightsky-*.html --no-filename | cut -d '>' -f 3 | cut -d '<' -f 1
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('nightsky: ' + 'parsing fail')
    for post in posts:
        appender(post, 'nightsky')

def pandora():
    stdlog('parser: ' + 'pandora')
    parser = '''
    grep '<span class="post-title gt-c-content-color-first">' source/pandora-*.html | cut -d '>' -f 2 | cut -d '<' -f 1
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('pandora: ' + 'parsing fail')
    for post in posts:
        appender(post, 'pandora')

def stormous():
    stdlog('parser: ' + 'stormous')
    # grep '<p> <h3> <font color="' source/stormous-*.html | grep '</h3>' | cut -d '>' -f 4 | cut -d '<' -f 1 | sed -e 's/^ *//g' -e 's/[[:space:]]*$//'
    # grep '<h3>' source/stormous-*.html | sed -e 's/^ *//g' -e 's/[[:space:]]*$//' | grep "^<h3> <font" | cut -d '>' -f 3 | cut -d '<' -f 1 | sed 's/[[:space:]]*$//'
    parser = '''
    awk '/<h3>/{getline; print}' source/stormous-*.html | sed -e 's/^ *//g' -e 's/[[:space:]]*$//'
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('stormous: ' + 'parsing fail')
    for post in posts:
        appender(post, 'stormous')

def leaktheanalyst():
    stdlog('parser: ' + 'leaktheanalyst')
    parser = '''
    grep '<label class="news-headers">' source/leaktheanalyst-*.html | cut -d '>' -f 2 | cut -d '<' -f 1 | sed -e 's/Section //' -e 's/#//' -e 's/^ *//g' -e 's/[[:space:]]*$//' | sort -n | uniq
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('leaktheanalyst: ' + 'parsing fail')
    for post in posts:
        appender(post, 'leaktheanalyst')

def kelvinsecurity():
    stdlog('parser: ' + 'kelvinsecurity')
    parser = '''
    egrep -o '<span style="font-size:20px;">([[:alnum:]]| |\.)+</span>' source/kelvinsecurity-*.html | cut -d '>' -f 2 | cut -d '<' -f 1
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('kelvinsecurity: ' + 'parsing fail')
    for post in posts:
        appender(post, 'kelvinsecurity')

def onyx():
    stdlog('parser: ' + 'onyx')
    parser = '''
    grep '<h6>' source/onyx-*.html | cut -d '>' -f 2 | cut -d '<' -f 1 | sed -e '/^[[:space:]]*$/d' -e '/Connect with us/d'
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('onyx: ' + 'parsing fail')
    for post in posts:
        appender(post, 'onyx')

def mindware():
    stdlog('parser: ' + 'mindware')
    parser = '''
    grep '<div class="card-header">' source/mindware-*.html | cut -d '>' -f 2 | cut -d '<' -f 1
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('mindware: ' + 'parsing fail')
    for post in posts:
        appender(post, 'mindware')


def cheers():
    stdlog('parser: ' + 'cheers')
    parser = '''
    grep '<a href="' source/cheers-*.html | grep -v title | cut -d '>' -f 2 | cut -d '<' -f 1 | sed -e '/Cheers/d' -e '/Home/d' -e 's/^ *//g' -e 's/[[:space:]]*$//'
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('cheers: ' + 'parsing fail')
    for post in posts:
        appender(post, 'cheers')

def yanluowang():
    stdlog('parser: ' + 'yanluowang')
    parser = '''
    grep '<a href="/posts' source/yanluowang-*.html | cut -d '>' -f 2 | cut -d '<' -f 1 | sed -e 's/^ *//g' -e 's/[[:space:]]*$//'
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('yanluowang: ' + 'parsing fail')
    for post in posts:
        appender(post, 'yanluowang')

#def omega():
#    stdlog('parser: ' + '0mega')
#    parser = '''
#    grep "<tr class='trow'>" -C 1 source/0mega-*.html | grep '<td>' | cut -d '>' -f 2 | cut -d '<' -f 1 | sort --uniq
#    '''
#    posts = runshellcmd(parser)
#    if len(posts) == 1:
#        errlog('0mega: ' + 'parsing fail')
#    for post in posts:
#        appender(post, '0mega')

def redalert():
    stdlog('parser: ' + 'redalert')
    parser = '''
    egrep -o "<h3>([A-Za-z0-9 ,\'.-])+</h3>" source/redalert-*.html | cut -d '>' -f 2 | cut -d '<' -f 1
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('redalert: ' + 'parsing fail')
    for post in posts:
        appender(post, 'redalert')

#def daixin():
#    stdlog('parser: ' + 'daixin')
#    parser = '''
#    grep '<h4 class="border-danger' source/daixin-*.html | cut -d '>' -f 3 | cut -d '<' -f 1 | sed -e 's/^ *//g' -e '/^$/d' -e 's/[[:space:]]*$//'
#    '''
#    posts = runshellcmd(parser)
#    if len(posts) == 1:
#        errlog('daixin: ' + 'parsing fail')
#    for post in posts:
#        appender(post, 'daixin')

def icefire():
    stdlog('parser: ' + 'icefire')
    parser = '''
    grep align-middle -C 2 source/icefire-*.html | grep span | grep -v '\*\*\*\*' | grep -v updating | grep '\*\.' | cut -d '>' -f 2 | cut -d '<' -f 1
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('icefire: ' + 'parsing fail')
    for post in posts:
        appender(post, 'icefire')

def donutleaks():
    stdlog('parser: ' + 'donutleaks')
    parser = '''
    grep '<h2 class="post-title">' source/donutleaks-*.html --no-filename | cut -d '>' -f 3 | cut -d '<' -f 1
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('donutleaks: ' + 'parsing fail')
    for post in posts:
        appender(post, 'donutleaks')
        
def sparta():
    stdlog('parser: ' + 'sparta')
    parser = '''
    grep 'class="card-header d-flex justify-content-between"><span>' source/sparta-*.html | cut -d '>' -f 4 | cut -d '<' -f 1 | sed -e '/^[[:space:]]*$/d' && grep '<div class="card-header d-flex justify-content-between"><span>' source/sparta-*.html | grep -v '<h2>' | cut -d '>' -f 3 | cut -d '<' -f 1 | sed -e 's/^ *//g' -e 's/[[:space:]]*$//'
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('sparta: ' + 'parsing fail')
    for post in posts:
        appender(post, 'sparta')

def qilin():
    stdlog('parser: ' + 'qilin')
    parser = '''
    grep 'class="item_box-info__link"' source/qilin-kb*.html | cut -d '"' -f 2 | sed '/#/d'
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('qilin: ' + 'parsing fail')
    for post in posts:
        appender(post, 'qilin')

def shaoleaks():
    stdlog('parser: ' + 'shaoleaks')
    parser = '''
    grep '<h2 class="entry-title' source/shaoleaks-*.html | cut -d '>' -f 3 | cut -d '<' -f 1
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('shaoleaks: ' + 'parsing fail')
    for post in posts:
        appender(post, 'shaoleaks')

def medusa():
    stdlog('parser: ' + 'medusa')
    parser = '''
    grep --no-filename '<h2 class="entry-title default-max-width">' source/medusa-*.html | cut -d '>' -f 3 | cut -d '<' -f 1
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('medusa: ' + 'parsing fail')
    for post in posts:
        appender(post, 'medusa')

def dataleak():
    stdlog('parser: ' + 'play')
    # %s '(?<=\\"\\").*?(?=div)' source/play-*.html | tr -d '<>' | tr -d \\'  | grep -v \?\? 
    parser = '''
    grep '<h2 class="post-title">' source/dataleak-*.html | cut -d '>' -f 2 | cut -d '<' -f 1
    '''
    posts = runshellcmd(parser)
    if len(posts) == 1:
        errlog('dataleak: ' + 'parsing fail')
    for post in posts:
        appender(post, 'dataleak')

def main():
    synack()
    everest()
    suncrypt()    
    lorenz()    
    lockbit2()    
    arvinclub()    
    avaddon()    
    xinglocker()    
    ragnarlocker()      
    revil()
    conti()    
    pysa()    
    nefilim()    
    mountlocker()    
    babuk()    
    ransomexx()    
    pay2key()    
    azroteam()    
    lockdata()    
    blacktor()    
    darkleakmarket()    
    blackmatter()    
    payloadbin()    
    groove()    
    bonacigroup()    
    karma()    
    spook()    
    quantum()    
    atomsilo()    
    lv()    
    five4bb47h()    
    midas()    
    marketo()    
    rook()    
    cryp70n1c0d3()    
    mosesstaff()    
    nightsky()    
    pandora()    
    stormous()    
    leaktheanalyst()    
    kelvinsecurity()    
    onyx()    
    mindware()    
    cheers()    
    yanluowang()    
    redalert()    
 #   daixin()    
    icefire()    
    donutleaks()    
    sparta()    
    qilin()    
    shaoleaks()    
    #medusa()    
    dataleak()    
