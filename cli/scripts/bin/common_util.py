import argparse
import json
import logging
import sys

import requests
from ratelimit import limits, sleep_and_retry

from cli.scripts.bin.constants import *

# Set Parse for Command Line Options
# parser = argparse.ArgumentParser()
# parser.add_argument("-e", "--env")
# parser.add_argument("-r", "--release")
# args = parser.parse_args()
# print(args)

# Logging conf
logging.basicConfig(
    stream=sys.stdout,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger()


def parse_json(file_path):
    f = open(os.path.join(CLI_BASE_DIR, file_path))
    data = json.load(f)
    f.close()
    return data


def parse_release(file_path):
    f = open(os.path.join(RELEASE_BASE_DIR, file_path))
    data = json.load(f)
    f.close()
    return data


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--env")
    parser.add_argument("-r", "--release")
    args = parser.parse_args()
    print(args)
    return args


def set_env():
    args = parse_args()
    if args.env:
        return parse_json(args.env)
    else:
        env_dict = {"baseUrl": os.environ.get("BASEURL"),
                    "accountId": os.environ.get("BOOMI_ACCOUNTID"),
                    "username": os.environ.get("BOOMI_USERNAME"),
                    "password": os.environ.get("BOOMI_PASSWORD"),
                    "environmentName": os.environ.get("ENVIRONMENT")}
        return env_dict


def set_release():
    args = parse_args()
    if args.release:
        return parse_json(args.release)
    else:
        release_file = os.environ.get("RELEASE_FILE")
        return parse_release(release_file)
        # raise Exception("Release file location not set.")


def log(message):
    logger.info(message)


@sleep_and_retry
@limits(calls=CALLS, period=RATE_LIMIT)
def check_limit():
    """ Empty function to check for calls to API """
    return


def requests_post(env, resource_path, payload):
    check_limit()
    logging.info("Request: {}".format(payload))
    base_url = env["baseUrl"]
    account_id = env["accountId"]
    username = env["username"]
    password = env["password"]
    headers = {"Accept": "application/json"}
    url = base_url + "/" + account_id + resource_path

    response = requests.post(url, auth=(
        username, password), json=payload, headers=headers)
    logging.info("Response: {}".format(response.text))
    response.raise_for_status()
    return response


def requests_delete(env, resource_path):
    check_limit()
    base_url = env["baseUrl"]
    account_id = env["accountId"]
    username = env["username"]
    password = env["password"]
    headers = {"Accept": "application/json"}
    url = base_url + "/" + account_id + resource_path

    response = requests.delete(url, auth=(
        username, password), headers=headers)
    logging.info("Response: {}".format(response.text))
    response.raise_for_status()
    return response
