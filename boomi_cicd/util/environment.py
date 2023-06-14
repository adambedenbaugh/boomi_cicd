from boomi_cicd.util.common_util import *


# https://help.boomi.com/bundle/developer_apis/page/r-atm-Environment_object.html


def query_environment(environment_name):
    """
    Query the Boomi environment by name to retrieve the environment ID.

    :param environment_name: The name of the Boomi environment.
    :type environment_name: str
    :return: The environment ID.
    :rtype: str
    :raises SystemExit: If the environment is not found.
    """
    resource_path = "/Environment/query"
    logging.info(resource_path)
    environment_query = "boomi_cicd/util/json/environmentQuery.json"
    payload = parse_json(environment_query)
    payload["QueryFilter"]["expression"]["argument"][0] = environment_name

    response = requests_post(resource_path, payload)

    json_response = json.loads(response.text)
    if json_response["numberOfResults"] == 0:
        logging.error(
            "Environment not found. EnvironmentName: {}".format(
                boomi_cicd.ENVIRONMENT_NAME
            )
        )
        sys.exit(1)
    environment_id = json_response["result"][0]["id"]
    return environment_id
