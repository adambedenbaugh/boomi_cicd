import argparse
import json
import logging
import os
import sys

import requests
from ratelimit import limits, sleep_and_retry
from retrying import retry

import boomi_cicd

if os.environ.get("AZURE_HTTP_USER_AGENT") is not None:
    # Logging conf
    # Azure DevOps already includes the date/time
    logging.basicConfig(
        stream=sys.stdout,
        format="%(levelname)-5s %(message)s",
        level=logging.DEBUG,
    )
else:
    logging.basicConfig(
        stream=sys.stdout,
        format="%(asctime)s.%(msecs)03d %(levelname)-5s %(message)s",
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
    """
    Parse a JSON file and return the parsed data.

    :param file_path: The path to the JSON file.
    :type file_path: str
    :return: The parsed data from the JSON file.
    :rtype: dict or list
    """
    f = open(os.path.join(boomi_cicd.CLI_BASE_DIR, file_path))
    data = json.load(f)
    f.close()
    return data


def parse_release(file_path):
    """
    Parse a release file and return the parsed data.

    :param file_path: The path to the release file.
    :type file_path: str
    :return: The parsed data from the release file.
    :rtype: dict
    """
    f = open(os.path.join(boomi_cicd.RELEASE_BASE_DIR, file_path))
    data = json.load(f)
    f.close()
    return data


def parse_args():
    """Will parse arguments from the command line. Looks for a release file with a -r or --release argument."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--release")
    args = parser.parse_args()
    return args


def set_release():
    """
    Set the release data based on command-line arguments or environment variable.

    This function retrieves the release data from either the command-line argument or the default configuration.
    If the `--release` argument is provided, it reads the JSON data from the specified file path.
    Otherwise, it reads the JSON data from the default release file path.

    :return: The release data as a dictionary.
    """
    args = parse_args()
    if args.release:
        return parse_json(args.release)
    else:
        release_file = boomi_cicd.RELEASE_FILE
        return parse_release(release_file)


@sleep_and_retry
@limits(calls=boomi_cicd.CALLS, period=boomi_cicd.RATE_LIMIT)
def check_limit():
    """
    Empty function to limit the number of calls to the Atomsphere API.

    This function is used as a decorator to enforce a rate limit on API calls. It ensures that the decorated function
    is called within the specified rate limit.

    :return: None
    """
    return


@retry(
    stop_max_attempt_number=3,
    wait_fixed=boomi_cicd.RATE_LIMIT_MILLISECONDS,
    retry_on_result=lambda x: x == 503,
)
def requests_get_xml(resource_path):
    """
    Perform a GET request to the Atomsphere API and retrieve XML data.

    :param resource_path: The resource path for the API endpoint.
    :type resource_path: str
    :return: The response object containing the XML data.
    :rtype: requests.Response
    :raises requests.HTTPError: If the GET request fails (non-2xx response). A 503 response will be retried up to 3 times.
    """
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


@retry(
    stop_max_attempt_number=3,
    wait_fixed=boomi_cicd.RATE_LIMIT_MILLISECONDS,
    retry_on_result=lambda x: x == 503,
)
def requests_get(resource_path):
    """
    Perform a GET request to the Atomsphere API and retrieve JSON data.

    :param resource_path: The resource path for the API endpoint.
    :type resource_path: str
    :return: The response object containing the JSON data.
    :rtype: requests.Response
    :raises requests.HTTPError: If the GET request fails (non-2xx response).  A 503 response will be retried up to 3 times.
    """
    check_limit()
    headers = {"Accept": "application/json"}
    url = boomi_cicd.BASE_URL + "/" + boomi_cicd.ACCOUNT_ID + resource_path

    response = requests.get(
        url, auth=(boomi_cicd.USERNAME, boomi_cicd.PASSWORD), headers=headers
    )
    logging.info("Response: {}".format(response.text))
    response.raise_for_status()
    return response


@retry(
    stop_max_attempt_number=3,
    wait_fixed=boomi_cicd.RATE_LIMIT_MILLISECONDS,
    retry_on_result=lambda x: x == 503,
)
def requests_post(resource_path, payload):
    """
    Perform a POST request to the Atomsphere API with the specified payload.

    :param resource_path: The resource path for the API endpoint.
    :type resource_path: str
    :param payload: The payload to be sent in the request body (as JSON).
    :type payload: dict
    :return: The response object containing the JSON response data.
    :rtype: requests.Response
    :raises requests.HTTPError: If the POST request fails (non-2xx response). A 503 response will be retried up to 3 times.
    """
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


@retry(
    stop_max_attempt_number=3,
    wait_fixed=boomi_cicd.RATE_LIMIT_MILLISECONDS,
    retry_on_result=lambda x: x == 503,
)
def requests_delete(resource_path):
    """
    Perform a DELETE request to the Atomsphere API.

    :param resource_path: The resource path for the API endpoint.
    :type resource_path: str
    :return: The response object containing the JSON response data.
    :rtype: requests.Response
    :raises requests.HTTPError: If the DELETE request fails (non-2xx response). A 503 response will be retried up to 3 times.
    """
    check_limit()
    headers = {"Accept": "application/json"}
    url = boomi_cicd.BASE_URL + "/" + boomi_cicd.ACCOUNT_ID + resource_path

    response = requests.delete(
        url, auth=(boomi_cicd.USERNAME, boomi_cicd.PASSWORD), headers=headers
    )
    logging.info("Response: {}".format(response.text))
    response.raise_for_status()
    return response
