import urllib2
import datetime
import json
import logging

from eduroam_abusers import *

def search_for_mac(days_back, mac):

    logging.debug("Searching for MAC %s", mac)
    now = datetime.datetime.now()
    search_mac = {"query":{"filtered":{"query":{"bool":{"should":[{"query_string":{"query":"*"}}]}},"filter":{"bool":{"must":[{"range":{"@timestamp":{"lt" : "now" }}},{"fquery":{"query":{"query_string":{"query":"tags:(\"eduroam\")"}},"_cache":"true"}},{"fquery":{"query":{"query_string":{"query":"mac:(\"whatever\")"}},"_cache":"true"}}]}}}},"highlight":{"fields":{},"fragment_size":2147483647,"pre_tags":["@start-highlight@"],"post_tags":["@end-highlight@"]},"size":500,"sort":[{"@timestamp":{"order":"desc","ignore_unmapped":"true"}},{"@timestamp":{"order":"desc","ignore_unmapped":"true"}}]}
    new_mac = 'mac:("%s")' % mac
    search_mac['query']['filtered']['filter']['bool']['must'][2]['fquery']['query']['query_string']['query'] = new_mac
    query_json = json.dumps(search_mac)
    users = {}
    for day_ago in range(days_back, -1, -1):
        logstash_url = "%slogstash-%d.%.2d.%.2d/_search?pretty=true" % (logstash_address, now.year, now.month, now.day-day_ago)
        req = urllib2.Request(logstash_url, query_json, {'Content-Type': 'application/json'})
        try:
            f = urllib2.urlopen(req, timeout=60)
        except:
            logging.critical("Networking issues!")
            return
        raw_response = f.read()
        response = json.loads(raw_response)
        for hit in response['hits']['hits']:
            if hit['_source']['user'] not in users:
                users[hit['_source']['user']] = 1
            else:
                users[hit['_source']['user']] += 1

            logging.debug("Found user {user} associated at {ap}".format(user=hit['_source']['user'], ap=hit['_source']['ap-name']))
    print "Found user {user} with {hits} hits when searching for {mac}".format(user=users.keys(), hits=users.values(), mac=mac)
    return users

def search_for_user(days_back, user):

    # FIXME: Finish implement
    ago = datetime.timedelta(hours=24)
    offset = (now - ago).isoformat()
    search_user = {"query":{"filtered":{"query":{"bool":{"should":[{"query_string":{"query":"*"}}]}},"filter":{"bool":{"must":[{"range":{"@timestamp":{"from":1456014984840,"to":1456187784840}}},{"fquery":{"query":{"query_string":{"query":"tags:(\"eduroam\")"}},"_cache":"true"}},{"fquery":{"query":{"query_string":{"query":"mac:(\"28:cf:e9:19:f1:57\")"}},"_cache":"true"}}]}}}},"highlight":{"fields":{},"fragment_size":2147483647,"pre_tags":["@start-highlight@"],"post_tags":["@end-highlight@"]},"size":500,"sort":[{"@timestamp":{"order":"desc","ignore_unmapped":"true"}},{"@timestamp":{"order":"desc","ignore_unmapped":"true"}}]}
    new_user = 'mac:("%s")' % user # needs fix
    search_user['query']['filtered']['filter']['bool']['must'][2]['fquery']['query']['query_string']['query'] = new_mac
    query_json = json.dumps(search_user)
    for day_ago in range(days_back, -1, -1):
        logstash_url2 = "%slogstash-%d.%.2d.%.2d/_search?pretty=true" % (logstash_url, now.year, now.month, now.day-day_ago)
        req = urllib2.Request(logstash_url2, query_json, {'Content-Type': 'application/json'})
        f = urllib2.urlopen(req)
        raw_response = f.read()
        response = json.loads(raw_response)
        users = {}