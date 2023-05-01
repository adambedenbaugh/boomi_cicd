from boomi_cicd.util.common_util import *


# https://help.boomi.com/bundle/developer_apis/page/r-atm-Packaged_Component_object.html

def create_packaged_component(env, release):
    resource_path = "/PackagedComponent"
    logging.info(resource_path)
    packaged_component_query = "boomi_cicd/util/json/createPackagedComponent.json"

    payload = parse_json(packaged_component_query)
    payload["componentId"] = release["componentId"]
    payload["packageVersion"] = release["packageVersion"]
    payload["notes"] = release["notes"]

    response = requests_post(env, resource_path, payload)

    package_id = json.loads(response.text)["packageId"]
    return package_id


def query_packaged_component(env, release):
    resource_path = "/PackagedComponent/query"
    logging.info(resource_path)
    logging.info("ComponentId: {}".format(release["componentId"]))
    logging.info("PackagedVersion: {}".format(release["packageVersion"]))
    packaged_component_query = "boomi_cicd/util/json/packagedComponentQuery.json"

    payload = parse_json(packaged_component_query)
    payload["QueryFilter"]["expression"]["nestedExpression"][0]["argument"][0] = release["componentId"]
    payload["QueryFilter"]["expression"]["nestedExpression"][1]["argument"][0] = release["packageVersion"]

    response = requests_post(env, resource_path, payload)

    package_id = ""
    if json.loads(response.text)["numberOfResults"] > 0:
        logging.info("Packaged component has already been created. ComponentId: {}, PackageId: {}".format(
            release["componentId"], release["packageVersion"]))
        package_id = json.loads(response.text)["result"][0]["packageId"]

    return package_id
