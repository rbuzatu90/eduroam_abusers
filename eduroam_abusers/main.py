from argparse import ArgumentParser
from edusearch import search_for_mac, search_for_user
from unifi import get_abusers
import logging
import keyring
import getpass

from eduroam_abusers import *

def main():

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
        keyring.set_password(app_name, app_user, password)

    else:
        password = keyring.get_password(app_name, app_user)
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
