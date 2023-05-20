import boomi_cicd
from boomi_cicd.util.atom import query_atom
from boomi_cicd.util.common_util import set_release
from boomi_cicd.util.process_schedules import (
    query_process_schedules,
    update_process_schedules,
)

# Open release json
releases = set_release()

# Get atom id
atom_id = query_atom(boomi_cicd.ATOM_NAME)

for release in releases["pipelines"]:
    component_id = release["componentId"]

    # Get conceptual id of deployed process
    conceptual_id = query_process_schedules(atom_id, component_id)

    update_process_schedules(
        component_id,
        conceptual_id,
        atom_id,
        release["schedule"] if "schedule" in release else None,
    )
