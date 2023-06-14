from boomi_cicd.util.common_util import *


# https://help.boomi.com/bundle/developer_apis/page/r-atm-Deployed_Package_object.html


def create_deployed_package(release, package_id, environment_id):
    """
    Create a deployed package in the Boomi environment.

    :param release: The release information.
    :type release: dict
    :param package_id: The ID of the package.
    :type package_id: str
    :param environment_id: The ID of the environment.
    :type environment_id: str
    :return: The deployment ID of the created package.
    :rtype: str
    """
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


def query_deployed_package(package_id, environment_id, currently_deployed=True):
    """
    Query the deployed package status in the Boomi environment.

    :param package_id: The ID of the package.
    :type package_id: str
    :param environment_id: The ID of the environment.
    :type environment_id: str
    :param currently_deployed: Flag indicating if currently deployed packages should be queried (default: True).
    :type currently_deployed: bool
    :return: True if the package has already been deployed, False otherwise.
    :rtype: bool
    """
    resource_path = "/DeployedPackage/query"
    environment_query = "boomi_cicd/util/json/deployedPackageQuery.json"
    payload = parse_json(environment_query)
    payload["QueryFilter"]["expression"]["nestedExpression"][0]["argument"][
        0
    ] = environment_id
    payload["QueryFilter"]["expression"]["nestedExpression"][1]["argument"][
        0
    ] = package_id
    # If active is True, then a query will be made for only active packages.
    # If active is missing, then a query will be made for all packages.
    if currently_deployed:
        active_status = {"argument": [True], "operator": "EQUALS", "property": "active"}
        payload["QueryFilter"]["expression"]["nestedExpression"].append(active_status)

    response = requests_post(resource_path, payload)

    number_of_results = json.loads(response.text)["numberOfResults"]
    if number_of_results:
        logging.info("Package has already been deployed.")
        return True
    else:
        return False


def delete_deployed_package(deployment_id):
    """
    Delete a deployed package in the Boomi environment.

    :param deployment_id: The ID of the deployment.
    :type deployment_id: str
    :return: The response text.
    :rtype: str
    """
    resource_path = "/DeployedPackage/{}".format(deployment_id)

    response = requests_delete(resource_path)
    return response.text
