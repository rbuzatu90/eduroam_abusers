import urllib2
import datetime
import json
from argparse import ArgumentParser
from unifi import get_abusers
import logging
import keyring
import getpass

def search_for_mac(days_back, mac):

    logging.debug("Searching for MAC %s", mac)
    ago = datetime.timedelta(hours=24)
    offset = (now - ago).isoformat()
    search_mac = {"query":{"filtered":{"query":{"bool":{"should":[{"query_string":{"query":"*"}}]}},"filter":{"bool":{"must":[{"range":{"@timestamp":{"from":"%s+03" % (offset, ), "to":"now"}}},{"fquery":{"query":{"query_string":{"query":"tags:(\"eduroam\")"}},"_cache":"true"}},{"fquery":{"query":{"query_string":{"query":"mac:(\"whatever\")"}},"_cache":"true"}}]}}}},"highlight":{"fields":{},"fragment_size":2147483647,"pre_tags":["@start-highlight@"],"post_tags":["@end-highlight@"]},"size":1000,"sort":[{"@timestamp":{"order":"desc","ignore_unmapped":"true"}},{"@timestamp":{"order":"desc","ignore_unmapped":"true"}}]}
    new_mac = 'mac:("%s")' % mac
    search_mac['query']['filtered']['filter']['bool']['must'][2]['fquery']['query']['query_string']['query'] = new_mac
    query_json = json.dumps(search_mac)
    users = {}
    for day_ago in range(days_back, -1, -1):
        logstash_url2 = "%slogstash-%d.%.2d.%.2d/_search?pretty=true" % (logstash_url, now.year, now.month, now.day-day_ago)
        print logstash_url2
        req = urllib2.Request(logstash_url2, query_json, {'Content-Type': 'application/json'})
        try:
            f = urllib2.urlopen(req, timeout=5)
        except:
            logging.critical("Networking issues")
            return
        raw_response = f.read()
        print raw_response
        response = json.loads(raw_response)
        for hit in response['hits']['hits']:
            if hit['_source']['user'] not in users:
                users[hit['_source']['user']] = 1
            else:
                users[hit['_source']['user']] += 1
            logging.info("Found user {user} associated at {ap}".format(user=hit['_source']['user'], ap=hit['_source']['ap-name']))
    return users

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

    app_name = "eduroam_abusers"

    parser = ArgumentParser(description="Easy logs")
    parser.add_argument('--verbose', '-v', action='count', default=None, help="The verbosity level. More v's means more logging")
    parser.add_argument("-P", "--password-prompt", default=False, action="store_true")
    subparser = parser.add_subparsers(title="Search options", dest="subcommand")
    mac = subparser.add_parser("mac")
    auto = subparser.add_parser("auto")
    user = subparser.add_parser("user")
    mac.add_argument("-m", "--mac", required=True, help="The MAC to search for", type=str)
    mac.add_argument("-d", "--days-back", required=False, help="Get logs from X days ago", type=int, default=0)
    auto.add_argument("-l", "--limit", required=False, help="Get users which have download more then X bytes", type=str, default="5GB")
    auto.add_argument("-d", "--days-back", required=False, help="Get logs from X days ago", type=int, default=2)
    args = parser.parse_args()

    password = None
    if args.password_prompt:
        password = getpass.getpass()
        keyring.set_password(app_name, "unifi", password)

    else:
        password = keyring.get_password(app_name, "unifi")
        if password is None:
            logging.critical("Enter a password")
            return

    if args.verbose is not None:
        if args.verbose > 4:
            log_level = 10
        else:
            log_level = 50 - args.verbose * 10
    else:
        log_level = 100
    logging.basicConfig(format='%(levelname)s:%(message)s', level=log_level)

    global logstash_url, now
    logstash_url="http://10.9.0.60:9200/"
    now = datetime.datetime.now()

    if args.subcommand == "mac":
        search_for_mac(args.days_back, args.mac)
    if args.subcommand == "user":
        search_for_user(args.days_back, args.user)
    if args.subcommand == "auto":
        abusers = []
        all_abusers = get_abusers(args.limit)
        if all_abusers:
            for user in all_abusers:
                x = search_for_mac(args.days_back, user)
                if x:
                    abusers.append(x)
        print abusers

if __name__ == '__main__':
        main()
