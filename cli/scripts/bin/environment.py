from cli.scripts.bin.common_util import *


def query_environment(env):
    resource_path = "/Environment/query"
    logging.info(resource_path)
    environment_query = os.path.join(env["workingDirectory"], "cli/scripts/json/environmentQuery.json")
    payload = parse_json(environment_query)
    payload["QueryFilter"]["expression"]["argument"][0] = env["environmentName"]

    response = requests_post(env, resource_path, payload)

    json_response = json.loads(response.text)
    if json_response["numberOfResults"] == 0:
        logging.error("Environment not found. EnvironmentName: {}".format(env["environmentName"]))
        sys.exit(1)
    environment_id = json_response["result"][0]["id"]
    return environment_id
