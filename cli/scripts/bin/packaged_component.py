from common_util import *
import requests


def create_packaged_component(env, release):
    base_url = env["baseUrl"]
    account_id = env["accountId"]
    username = env["username"]
    password = env["password"]
    atom_query_name = ["Test Atom Cloud"]
    headers = { "Accept": "application/json"}

    url = base_url + "/" + account_id + "/PackagedComponent"
    print("Component Id Query URL: {}".format(url))

    packaged_component_query = "cli/scripts/json/createPackagedComponent.json"

    query = parse_json(packaged_component_query)
    query["componentId"] = release["componentId"]
    query["packageVersion"] = release["packageVersion"]
    query["notes"] = release["notes"]

    print(query)
    response = requests.post(url, auth=(
        username, password), json=query, headers=headers)

    print(json.loads(response.text))
    package_id = json.loads(response.text)["packageId"]
    return package_id  



def query_packaged_component(env, release):
    base_url = env["baseUrl"]
    account_id = env["accountId"]
    username = env["username"]
    password = env["password"]
    headers = { "Accept": "application/json"}

    url = base_url + "/" + account_id + "/PackagedComponent/query"
    print("Component Id Query URL: {}".format(url))

    packaged_component_query = "cli/scripts/json/queryPackagedComponent.json"

    query = parse_json(packaged_component_query)
    query["QueryFilter"]["expression"]["nestedExpression"][0]["argument"][0] = release["componentId"]
    query["QueryFilter"]["expression"]["nestedExpression"][1]["argument"][0] = release["packageVersion"]

    print(query)
    response = requests.post(url, auth=(
        username, password), json=query, headers=headers)

    package_id = ""
    print(json.loads(response.text))
    if json.loads(response.text)["numberOfResults"] > 0:
        package_id = json.loads(response.text)["result"][0]["packageId"]
    
    return package_id  
  