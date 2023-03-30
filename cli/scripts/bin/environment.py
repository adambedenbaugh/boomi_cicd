from common_util import *
import requests


def query_environment(env):

    resource_path = "/Environment/query"
    # print("Component Id Query URL: {}".format(url))

    environment_query = "cli/scripts/json/queryEnvironment.json"

    payload = parse_json(environment_query)
    payload["QueryFilter"]["expression"]["argument"][0] = env["environmentName"]

    print(payload)
    print("---------")
    response = requests_post(env, resource_path, payload)

    print(json.loads(response.text))
    environment_id = json.loads(response.text)["result"][0]["id"]
    return environment_id  
