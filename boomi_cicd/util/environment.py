from boomi_cicd.util.common_util import *


# https://help.boomi.com/bundle/developer_apis/page/r-atm-Environment_object.html


def query_environment():
    resource_path = "/Environment/query"
    logging.info(resource_path)
    environment_query = os.path.join(
        boomi_cicd.WORKING_DIRECTORY, "boomi_cicd/util/json/environmentQuery.json"
    )
    payload = parse_json(environment_query)
    payload["QueryFilter"]["expression"]["argument"][0] = boomi_cicd.ENVIRONMENT_NAME

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
