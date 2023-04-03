from common_util import *


def query_atom(env):

    resource_path = "/Atom/query"
    environment_query = "cli/scripts/json/atomQuery.json"

    payload = parse_json(environment_query)
    payload["QueryFilter"]["expression"]["argument"][0] = env["atomName"]

    response = requests_post(env, resource_path, payload)

    atom_id = json.loads(response.text)["result"][0]["id"]
    return atom_id  
