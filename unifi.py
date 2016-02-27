from cookielib import CookieJar
import urllib2
import ssl
import json
import math
from re import search
import logging
ssl._create_default_https_context = ssl._create_unverified_context

global login_url, data_url, data
login_url = 'https://10.3.0.2:8443/api/login'
data_url = 'https://10.3.0.2:8443/api/s/default/stat/alluser?pretty=true'
data = '{"username":"admin","password":"aihechahtahLieX8shie","strict":true}'

def get_cookie():

    logging.debug('Getting cookie')
    cj = CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    try:
        response = opener.open(login_url, data, timeout=5)
    except:
        logging.critical("Networking issues")
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
    val = 1024 ** power
    size = new_size * val
    return size


def get_abusers(limit):

    my_cookie = get_cookie()
    if not my_cookie:
        return
    req2 = urllib2.Request(data_url)
    req2.add_header('Cookie', my_cookie)
    logging.debug("Reading from HTTP stream, please wait")
    response = urllib2.urlopen(req2)
    all_users = json.loads(response.read())
    abusers = []
    user_no_value = 0
    user_count = 0
    for user in all_users['data']:
        if user.has_key('oui') and user.has_key('hostname') and user.has_key('stat'):
            if user['stat']['rx_bytes'] >= h2bytes(limit):
                abusers.append(user['mac'])
                user_count += 1
                logging.info("Abuser OUI {oui}, hostname {hostname}, MAC {mac} uploaded size {tx}, downloaded size {rx}"\
                             .format(oui=user['oui'], hostname=user['hostname'], mac=user['mac'], tx=bytes2h(user['stat']['tx_bytes']), rx=bytes2h(user['stat']['rx_bytes'])))
        else:
            logging.debug("Missing some values on user {user}".format(user=user['oui']))
            user_no_value += 1
    logging.info("Total users with missing values {no}".format(no=user_no_value))
    logging.info("Total user count that exceed {limit} limit is {count}".format(limit=limit, count=user_count))
    return abusers
