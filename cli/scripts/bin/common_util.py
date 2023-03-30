import json
import requests
import yaml


def parse_json(file_path):
    f = open(file_path)
    data = json.load(f)
    f.close()
    return data


def parse_yaml(file_path):
    f = open(file_path, "r")
    data = yaml.safe_load(f)
    f.close()
    return data


def log_header(label):
    line = ""
    line += "-" * 100
    print(line)
    print(label)
    print(line)

# Update this to use Python's standard logger


def log(label):
    line = ""
    line += "-" * 100
    print(line)
    print(label)
    print(line)


def requests_post(env, resource_path, payload):
    base_url = env["baseUrl"]
    account_id = env["accountId"]
    username = env["username"]
    password = env["password"]
    headers = {"Accept": "application/json"}
    url = base_url + "/" + account_id + resource_path

    return requests.post(url, auth=(
        username, password), json=payload, headers=headers)
