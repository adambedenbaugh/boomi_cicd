from common_util import *
import requests


def query_environment(env):
    
    resource_path = "/Environment/query"
    logging.info(resource_path)
    environment_query = "cli/scripts/json/environmentQuery.json"
    payload = parse_json(environment_query)
    payload["QueryFilter"]["expression"]["argument"][0] = env["environmentName"]

    response = requests_post(env, resource_path, payload)

    # write log to test if there is an environment returned.

    json_response = json.loads(response.text)
    environment_id = json_response["result"][0]["id"]
    return environment_id  
