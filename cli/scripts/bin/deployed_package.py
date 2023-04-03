from common_util import *


def create_deployed_package(env, release, package_id, environment_id):

    resource_path = "/DeployedPackage"
    environment_query = "cli/scripts/json/deployedPackageCreate.json"
    payload = parse_json(environment_query)
    payload["environmentId"] = environment_id
    payload["packageId"] = package_id
    payload["notes"] = release["notes"]
    if "listenerStatus" in release:
        payload["listenerStatus"] = release["listenerStatus"]

    response = requests_post(env, resource_path, payload)

    return True


def query_deployed_package(env, release, package_id, environment_id):

    resource_path = "/DeployedPackage/query"
    environment_query = "cli/scripts/json/deployedPackageQuery.json"
    payload = parse_json(environment_query)
    payload["QueryFilter"]["expression"]["nestedExpression"][0]["argument"][0] = environment_id
    payload["QueryFilter"]["expression"]["nestedExpression"][1]["argument"][0] = package_id

    response = requests_post(env, resource_path, payload) 

    number_of_results = json.loads(response.text)["numberOfResults"]
    if number_of_results:
        logging.info("Package has already been deployed.")
        return True
    else:
        return False
