from boomi_cicd.util.common_util import *


# https://help.boomi.com/bundle/developer_apis/page/r-atm-Process_Schedules_object.html

def query_process_schedules(env, atom_id, process_id):
    resource_path = "/ProcessSchedules/query"
    process_schedule_query = os.path.join(env["workingDirectory"], "boomi_cicd/util/json/processScheduleQuery.json")

    payload = parse_json(process_schedule_query)
    payload["QueryFilter"]["expression"]["nestedExpression"][0]["argument"][0] = atom_id
    payload["QueryFilter"]["expression"]["nestedExpression"][1]["argument"][0] = process_id

    response = requests_post(env, resource_path, payload)

    json_response = json.loads(response.text)
    if json_response["numberOfResults"] == 0:
        logging.error("Process is not deployed. Atom Name: {}, Process Id: {}".format(env["atomName"], process_id))
        sys.exit(1)
    conceptual_id = json.loads(response.text)["result"][0]["id"]
    return conceptual_id


def update_process_schedules(env, component_id, conceptual_id, atom_id, schedules):
    resource_path = "/ProcessSchedules/{}/update".format(conceptual_id)
    process_schedule_updated = os.path.join(env["workingDirectory"], "boomi_cicd/util/json/processScheduleUpdate.json")

    payload = parse_json(process_schedule_updated)
    payload["processId"] = component_id
    payload["atomId"] = atom_id
    payload["id"] = conceptual_id

    # If schedules is empty, then clear the schedules.
    # If not empty, then update the schedules.
    if schedules is not None:
        schedules = schedules.split(";")

        for schedule in schedules:
            split_schedule = schedule.strip().split(" ")
            if len(split_schedule) is not 6:
                logging.error(
                    "Invalid schedule format. Format: {}. Arguments passed: {}. Arguments expected: 6.".format(schedule,
                                                                                                               len(split_schedule)))
                sys.exit(1)
            json_variable = {
                "@type": "Schedule",
                "minutes": split_schedule[0],
                "hours": split_schedule[1],
                "daysOfWeek": split_schedule[2],
                "daysOfMonth": split_schedule[3],
                "months": split_schedule[4],
                "years": split_schedule[5],
            }

            if payload["Schedule"]:
                payload["Schedule"].append(json_variable)
            else:
                payload["Schedule"] = [json_variable]

    response = requests_post(env, resource_path, payload)

    json_response = json.loads(response.text)
    # if json_response["numberOfResults"] == 0:
    #     logging.error("Process is not deployed. Atom Name: {}, Process Id: {}".format(env["atomName"], process_id))
    #     sys.exit(1)
    # conceptual_id = json.loads(response.text)["result"][0]["id"]
    return "to be replaced"