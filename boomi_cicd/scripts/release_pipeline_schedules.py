from boomi_cicd.util.atom import *
from boomi_cicd.util.process_schedules import *

# Open environment variables
# command line: -e
env = set_env()
# Open release json
# command line: -r
releases = set_release()

# Get atom id
atom_id = query_atom(env, env["atomName"])

for release in releases["pipelines"]:
    component_id = release["componentId"]

    # Get conceptual id of deployed process
    conceptual_id = query_process_schedules(env, atom_id, component_id)

    update_process_schedules(env, component_id, conceptual_id, atom_id,
                             release["schedule"] if "schedule" in release else None)
