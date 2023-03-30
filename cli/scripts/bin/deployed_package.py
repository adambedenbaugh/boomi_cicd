from common_util import *
import requests


def create_deployed_package(env, release, package_id, environment_id):

    resource_path = "/DeployedPackage"

    environment_query = "cli/scripts/json/createDeployedPackage.json"

    payload = parse_json(environment_query)
    payload["environmentId"] = environment_id
    payload["packageId"] = package_id
    payload["notes"] = release["notes"]
    if "listenerStatus" in release:
        payload["listenerStatus"] = release["listenerStatus"]

    print(payload)
    response = requests_post(env, resource_path, payload)
    
    print(response.status_code)
    print(json.loads(response.text))
    if response.status_code == 200:
        return True
    else:
        raise Exception("Deployment Failed for {}. Status Code: {}, Error Message: {}".format(
            release["processName"], response.status_code, json.loads(response.text)))


def query_deployed_package(env, release, package_id, environment_id):

    resource_path = "/DeployedPackage/query"

    environment_query = "cli/scripts/json/queryDeployedPackage.json"

    payload = parse_json(environment_query)
    payload["QueryFilter"]["expression"]["nestedExpression"][0]["argument"][0] = environment_id
    payload["QueryFilter"]["expression"]["nestedExpression"][1]["argument"][0] = package_id

    print(payload)
    response = requests_post(env, resource_path, payload) 

    print(response.status_code)
    print(json.loads(response.text))
    number_of_results = json.loads(response.text)["numberOfResults"]
    if number_of_results:
        return True
    else:
        return False
