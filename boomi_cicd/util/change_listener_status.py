from boomi_cicd.util.common_util import *


# https://help.boomi.com/bundle/developer_apis/page/r-atm-Change_listener_status.html


def change_listener_status(listener_id, atom_id, action):
    resource_path = "/changeListenerStatus"
    change_listener_status_json = os.path.join(
        boomi_cicd.WORKING_DIRECTORY, "boomi_cicd/util/json/changeListenerStatus.json"
    )

    payload = parse_json(change_listener_status_json)
    payload["listenerId"] = listener_id
    payload["containerId"] = atom_id
    payload["action"] = action

    response = requests_post(resource_path, payload)
    # If successful, the response will return a 200 and the response empty.
    # Any other response will throw an error within requests_post()
    return True
