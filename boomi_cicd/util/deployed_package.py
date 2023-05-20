from boomi_cicd.util.common_util import *


# https://help.boomi.com/bundle/developer_apis/page/r-atm-Deployed_Package_object.html


def create_deployed_package(release, package_id, environment_id):
    resource_path = "/DeployedPackage"
    environment_query = "boomi_cicd/util/json/deployedPackageCreate.json"
    payload = parse_json(environment_query)
    payload["environmentId"] = environment_id
    payload["packageId"] = package_id
    payload["notes"] = release["notes"]
    payload["listenerStatus"] = release.get("listenerStatus")

    if "listenerStatus" in release:
        payload["listenerStatus"] = release["listenerStatus"]

    response = requests_post(resource_path, payload)

    return json.loads(response.text)["deploymentId"]


def query_deployed_package(package_id, environment_id):
    resource_path = "/DeployedPackage/query"
    environment_query = "boomi_cicd/util/json/deployedPackageQuery.json"
    payload = parse_json(environment_query)
    payload["QueryFilter"]["expression"]["nestedExpression"][0]["argument"][
        0
    ] = environment_id
    payload["QueryFilter"]["expression"]["nestedExpression"][1]["argument"][
        0
    ] = package_id

    response = requests_post(resource_path, payload)

    number_of_results = json.loads(response.text)["numberOfResults"]
    if number_of_results:
        logging.info("Package has already been deployed.")
        return True
    else:
        return False


def delete_deployed_package(deployment_id):
    resource_path = "/DeployedPackage/{}".format(deployment_id)

    response = requests_delete(resource_path)
    return response.text
