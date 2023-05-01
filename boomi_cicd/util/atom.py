from boomi_cicd.util.common_util import *


# https://help.boomi.com/bundle/developer_apis/page/r-atm-Atom_object.html

def query_atom(env, atom_name):
    resource_path = "/Atom/query"
    environment_query = os.path.join(env["workingDirectory"], "boomi_cicd/util/json/atomQuery.json")

    payload = parse_json(environment_query)
    payload["QueryFilter"]["expression"]["argument"][0] = atom_name

    response = requests_post(env, resource_path, payload)

    json_response = json.loads(response.text)
    if json_response["numberOfResults"] == 0:
        logging.error("Atom not found. atomname: {}".format(env["atomName"]))
        sys.exit(1)
    atom_id = json.loads(response.text)["result"][0]["id"]
    return atom_id
