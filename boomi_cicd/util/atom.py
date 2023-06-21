from boomi_cicd.util.common_util import *


# https://help.boomi.com/bundle/developer_apis/page/r-atm-Atom_object.html

def query_atom(atom_name):
    """
    Query the Atom by name and retrieve its ID.

    This function sends a request to the AtomSphere API to query for an Atom
    with the specified name. If the Atom is found, then an ID is returned. If no
    atom is found then an error is logged and the program exits.

    :param atom_name: The name of the Atom to query.
    :type atom_name: str
    :return: The ID of the queried Atom.
    :rtype: str
    """
    resource_path = "/Atom/query"
    environment_query = "boomi_cicd/util/json/atomQuery.json"

    payload = parse_json(environment_query)
    payload["QueryFilter"]["expression"]["argument"][0] = atom_name

    response = requests_post(resource_path, payload)

    json_response = json.loads(response.text)
    if json_response["numberOfResults"] == 0:
        logging.error("Atom not found. atomname: {}".format(boomi_cicd.ATOM_NAME))
        sys.exit(1)
    atom_id = json.loads(response.text)["result"][0]["id"]
    return atom_id
