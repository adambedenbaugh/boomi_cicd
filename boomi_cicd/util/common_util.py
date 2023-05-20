import argparse
import json
import logging
import os
import sys

import requests
from ratelimit import limits, sleep_and_retry

import boomi_cicd

# Logging conf
logging.basicConfig(
    stream=sys.stdout,
    format="%(asctime)s.%(msecs)03d %(levelname)s %(message)s",
    level=logging.DEBUG,
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger()

header = """
    __                                                __
   / /_  ____  ____  ____ ___  (_)   _____(_)________/ /
  / __ \/ __ \/ __ \/ __ `__ \/ /   / ___/ / ___/ __  /
 / /_/ / /_/ / /_/ / / / / / / /   / /__/ / /__/ /_/ /
/_.___/\____/\____/_/ /_/ /_/_/____\___/_/\___/\__,_/
                             /_____/                              
"""
for line in header.splitlines():
    logger.info(line)


def parse_json(file_path):
    f = open(os.path.join(boomi_cicd.CLI_BASE_DIR, file_path))
    data = json.load(f)
    f.close()
    return data


def parse_release(file_path):
    f = open(os.path.join(boomi_cicd.RELEASE_BASE_DIR, file_path))
    data = json.load(f)
    f.close()
    return data


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--release")
    args = parser.parse_args()
    return args


def set_release():
    args = parse_args()
    if args.release:
        return parse_json(args.release)
    else:
        release_file = boomi_cicd.RELEASE_FILE
        return parse_release(release_file)


@sleep_and_retry
@limits(calls=boomi_cicd.CALLS, period=boomi_cicd.RATE_LIMIT)
def check_limit():
    """Empty function to check for calls to Atomsphere API"""
    return


def requests_get_xml(resource_path):
    check_limit()
    headers = {"Accept": "application/xml"}
    url = boomi_cicd.BASE_URL + "/" + boomi_cicd.ACCOUNT_ID + resource_path

    response = requests.get(
        url, auth=(boomi_cicd.USERNAME, boomi_cicd.PASSWORD), headers=headers
    )
    logging.info(
        "Response: {}".format(response.text.replace("\r", "").replace("\n", ""))
    )
    response.raise_for_status()
    return response


def requests_get(resource_path):
    check_limit()
    headers = {"Accept": "application/json"}
    url = boomi_cicd.BASE_URL + "/" + boomi_cicd.ACCOUNT_ID + resource_path

    response = requests.get(
        url, auth=(boomi_cicd.USERNAME, boomi_cicd.PASSWORD), headers=headers
    )
    logging.info("Response: {}".format(response.text))
    response.raise_for_status()
    return response


def requests_post(resource_path, payload):
    check_limit()
    logging.info("Request: {}".format(json.dumps(payload)))
    headers = {"Accept": "application/json"}
    url = boomi_cicd.BASE_URL + "/" + boomi_cicd.ACCOUNT_ID + resource_path

    response = requests.post(
        url,
        auth=(boomi_cicd.USERNAME, boomi_cicd.PASSWORD),
        json=payload,
        headers=headers,
    )
    logging.info("Response: {}".format(response.text))
    response.raise_for_status()
    return response


def requests_delete(resource_path):
    check_limit()
    headers = {"Accept": "application/json"}
    url = boomi_cicd.BASE_URL + "/" + boomi_cicd.ACCOUNT_ID + resource_path

    response = requests.delete(
        url, auth=(boomi_cicd.USERNAME, boomi_cicd.PASSWORD), headers=headers
    )
    logging.info("Response: {}".format(response.text))
    response.raise_for_status()
    return response
