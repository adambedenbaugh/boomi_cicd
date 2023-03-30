from common_util import *
import requests


# Open variables
# env = parse_json("local/env.json")



def query_atom_id(env):
    base_url = env["baseUrl"]
    account_id = env["accountId"]
    username = env["username"]
    password = env["password"]
    atom_query_name = ["Test Atom Cloud"]
    headers = {"Accept": "application/json"}
    # Query for Atom Id to Execution On
    atom_id_url = base_url + "/" + account_id + "/Atom/query"
    log("Atom ID")
    print("Atom Id Query URL: {}".format(atom_id_url))

    atom_id_query = "cli/scripts/json/queryAtom.json"

    query = parse_json(atom_id_query)
    query["QueryFilter"]["expression"]["argument"] = atom_query_name

    response = requests.post(atom_id_url, auth=(
        username, password), json=query, headers=headers)

    atom_id = json.loads(response.text)["result"][0]["id"]
    return atom_id