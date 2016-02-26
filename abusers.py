import urllib2
import datetime
import json
import argparse
from argparse import ArgumentParser
from unifi import get_abusers


def search_for_mac(days_back, mac):

    ago = datetime.timedelta(hours=24)
    offset = (now - ago).isoformat()
    search_mac = {"query":{"filtered":{"query":{"bool":{"should":[{"query_string":{"query":"*"}}]}},"filter":{"bool":{"must":[{"range":{"@timestamp":{"from":"%s+03" % (offset, ), "to":"now"}}},{"fquery":{"query":{"query_string":{"query":"tags:(\"eduroam\")"}},"_cache":"true"}},{"fquery":{"query":{"query_string":{"query":"mac:(\"whatever\")"}},"_cache":"true"}}]}}}},"highlight":{"fields":{},"fragment_size":2147483647,"pre_tags":["@start-highlight@"],"post_tags":["@end-highlight@"]},"size":1000,"sort":[{"@timestamp":{"order":"desc","ignore_unmapped":"true"}},{"@timestamp":{"order":"desc","ignore_unmapped":"true"}}]}
    new_mac = 'mac:("%s")' % mac
    search_mac['query']['filtered']['filter']['bool']['must'][2]['fquery']['query']['query_string']['query'] = new_mac
    query_json = json.dumps(search_mac)
    for day_ago in range(days_back, -1, -1):
        logstash_url2 = "%slogstash-%d.%.2d.%.2d/_search?pretty=true" % (logstash_url, now.year, now.month, now.day-day_ago)
        req = urllib2.Request(logstash_url2, query_json, {'Content-Type': 'application/json'})
        f = urllib2.urlopen(req)
        raw_response = f.read()
        response = json.loads(raw_response)
        users = {}
        for hit in response['hits']['hits']:
            if hit['_source']['user'] not in users:
                users[hit['_source']['user']] = 1
            else:
                users[hit['_source']['user']] += 1
            print "Found user", hit['_source']['user'], "associated at AP", hit['_source']['ap-name']
    print users

def search_for_user(days_back, user): # minor fix needed

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

        # to be continued

def main():

    parser = ArgumentParser(description="Easy logs")
    subparser = parser.add_subparsers(title="Search options", dest="subcommand")
    mac = subparser.add_parser("mac")
    user = subparser.add_parser("user")
    mac.add_argument("-m", "--mac", required=True, help="The MAC to search for", type=str)
    mac.add_argument("-d", "--days-back", required=False, help="The MAC to search for", type=int, default=0)
    args = parser.parse_args()

    global logstash_url, now
    logstash_url="http://10.9.0.60:9200/"
    now = datetime.datetime.now()

    if args.subcommand == "mac":
        search_for_mac(args.days_back, args.mac)
    if args.subcommand == "user":
        search_for_user(args.days_back, args.user)


if __name__ == '__main__':
        main()
