from common_util import *


def query_atom_id(env, atom_name):
    resource_path = "/Atom/query"
    atom_id_query = "cli/scripts/json/atomQuery.json"

    payload = parse_json(atom_id_query)
    payload["QueryFilter"]["expression"]["argument"] = atom_name

    response = requests_post(env, resource_path, payload)

    atom_id = json.loads(response.text)["result"][0]["id"]
    return atom_id
