from cookielib import CookieJar
import urllib2
import ssl
import json
import math
from re import search
ssl._create_default_https_context = ssl._create_unverified_context

global login_url, data_url, data
login_url = 'https://10.3.0.2:8443/api/login'
data_url = 'https://10.3.0.2:8443/api/s/default/stat/alluser?pretty=true'
data = '{"username":"admin","password":"aihechahtahLieX8shie","strict":true}'

def get_cookie():

    cj = CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    try:
        response = opener.open(login_url, data, timeout=5)
    except:
        print "Networking issues"
        return
    content = response.read()
    return response.headers.get('Set-Cookie')


def bytes2h(size):

    if (size == 0):
        return '0B'
    size_name = ("b","KB", "MB", "GB", "TB")
    i = int(math.floor(math.log(size,1024)))
    p = math.pow(1024,i)
    s = round(size/p,2)
    return '%s %s' % (s,size_name[i])


def h2bytes(size):

    new_size = int(search(r'\d+', size).group())
    str_part= search(r'[kmgtb]+', size.lower()).group()
    size_name = ["b", "kb", "mb", "gb", "gb", "tb"]
    power = size_name.index(str_part)
    val = new_size * 1024 ** power
    size = new_size * val
    return size


def get_abusers(limit):

    my_cookie = get_cookie()
    if not my_cookie:
        return
    req2 = urllib2.Request(data_url)
    req2.add_header('Cookie', my_cookie)
    response = urllib2.urlopen(req2)
    all_users = json.loads(response.read())
    abusers = []
    user_no_value = 0
    for user in all_users['data']:
        if user.has_key('oui') and user.has_key('hostname') and user.has_key('stat'):
            abusers.append(user['mac'])
            print user['oui'], user['hostname'], bytes2h(user['stat']['tx_bytes']), bytes2h(user['stat']['rx_bytes'])
        else:
            print "Missing some values on user", user['oui']
            user_no_value += 1
    print "Total users with missing values", user_no_value
    return abusers
