import boomi_cicd
from boomi_cicd.util.atom import query_atom
from boomi_cicd.util.change_listener_status import change_listener_status
from boomi_cicd.util.common_util import set_release
from boomi_cicd.util.process_schedule_status import (
    query_process_schedule_status,
    update_process_schedule_status,
)

# This script is used to turn off listener and batch schedules in primary atom and on in DR
# The atoms are set up in an active-active configuration within the same environment
# No persisted properties are being used on the primary atom

# Open release json
releases = set_release()

# Get atom id
atom_id = query_atom(boomi_cicd.ATOM_NAME)
atom_dr_id = query_atom(boomi_cicd.ATOM_NAME_DR)

for release in releases["pipelines"]:
    component_id = release["componentId"]
    # Turn off listener in primary and on in DR
    if "listenerStatus" in release:
        change_listener_status(component_id, atom_id, "pause")
        change_listener_status(component_id, atom_id, "resume")

    # Pause schedules in primary and resume in DR
    if "schedule" in release:
        # Get conceptual id of deployed process
        conceptual_id = query_process_schedule_status(atom_id, component_id)
        conceptual_id_dr = query_process_schedule_status(atom_dr_id, component_id)

        update_process_schedule_status(component_id, conceptual_id, atom_id, False)
        update_process_schedule_status(component_id, conceptual_id_dr, atom_dr_id, True)
