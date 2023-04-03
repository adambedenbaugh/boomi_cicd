import argparse
from constants import *
import json
import logging
from ratelimit import limits, sleep_and_retry
import requests
import sys
import yaml


# Set Parse for Command Line Options
parser = argparse.ArgumentParser()
parser.add_argument("-e", "--env")
parser.add_argument("-r", "--release")
args = parser.parse_args()

# Logging conf
logging.basicConfig(
    stream=sys.stdout,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger()



def parse_json(file_path):
    f = open(DIRECTORY_BASE + file_path)
    data = json.load(f)
    f.close()
    return data


def parse_yaml(file_path):
    f = open(file_path, "r")
    data = yaml.safe_load(f)
    f.close()
    return data


def set_env():
    if args.env:
        return parse_json(args.env)
    else:
        # Populate dict with environment variables
        print("todo")


def set_release():
    if args.release:
        return parse_json(args.release)



def log_header(label):
    line = ""
    line += "-" * 100
    print(line)
    print(label)
    print(line)


# Update this to use Python's standard logger


def log(message):
    logger.info(message)


@sleep_and_retry
@limits(calls=CALLS, period=RATE_LIMIT)
def check_limit():
    ''' Empty function just to check for calls to API '''
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
