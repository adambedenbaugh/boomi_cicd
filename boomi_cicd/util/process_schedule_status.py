from boomi_cicd.util.common_util import *


# https://help.boomi.com/bundle/developer_apis/page/r-atm-Project_Schedule_Status_object.html


def query_process_schedule_status(atom_id, process_id):
    """
    Query the process schedule status to check if the process is deployed.

    :param atom_id: The ID of the Atom.
    :type atom_id: str
    :param process_id: The ID of the process.
    :type process_id: str
    :return: The conceptual ID of the deployed process.
    :rtype: str
    :raises: SystemExit: If the process is not deployed.
    """
    resource_path = "/ProcessScheduleStatus/query"
    process_schedule_query = os.path.join(
        boomi_cicd.WORKING_DIRECTORY,
        "boomi_cicd/util/json/processScheduleStatusQuery.json",
    )

    payload = parse_json(process_schedule_query)
    payload["QueryFilter"]["expression"]["nestedExpression"][0]["argument"][0] = atom_id
    payload["QueryFilter"]["expression"]["nestedExpression"][1]["argument"][
        0
    ] = process_id

    response = requests_post(resource_path, payload)

    json_response = json.loads(response.text)
    if json_response["numberOfResults"] == 0:
        logging.error(
            "Process is not deployed. Atom Name: {}, Process Id: {}".format(
                boomi_cicd.ATOM_NAME, process_id
            )
        )
        sys.exit(1)
    conceptual_id = json.loads(response.text)["result"][0]["id"]
    return conceptual_id


def update_process_schedule_status(component_id, conceptual_id, atom_id, enabled):
    """
    Update the process schedule status.

    :param component_id: The ID of the component.
    :type component_id: str
    :param conceptual_id: The conceptual ID of the process schedule.
    :type conceptual_id: str
    :param atom_id: The ID of the Atom.
    :type atom_id: str
    :param enabled: Indicates whether the process schedule should be enabled or disabled.
    :type enabled: bool
    :return: True if the process schedule status update is successful.
    :rtype: bool
    """
    resource_path = "/ProcessScheduleStatus/{}/update".format(conceptual_id)
    process_schedule_updated = os.path.join(
        boomi_cicd.WORKING_DIRECTORY,
        "boomi_cicd/util/json/processScheduleStatusUpdate.json",
    )

    payload = parse_json(process_schedule_updated)
    payload["processId"] = component_id
    payload["atomId"] = atom_id
    payload["id"] = conceptual_id
    payload["enabled"] = enabled

    requests_post(resource_path, payload)

    return True
