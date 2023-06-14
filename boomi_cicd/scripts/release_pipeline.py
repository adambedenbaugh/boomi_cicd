from boomi_cicd.util.atom import query_atom
from boomi_cicd.util.deployed_package import *
from boomi_cicd.util.environment import query_environment
from boomi_cicd.util.packaged_component import query_packaged_component, create_packaged_component
from boomi_cicd.util.process_schedules import query_process_schedules, update_process_schedules

# Open release json
releases = set_release()

environment_id = query_environment(boomi_cicd.ENVIRONMENT_NAME)
atom_id = query_atom(boomi_cicd.ATOM_NAME)

for release in releases["pipelines"]:
    component_id = release["componentId"]
    process_name = release["processName"]
    package_version = release["packageVersion"]
    notes = release.get("notes")

    package_id = query_packaged_component(component_id, package_version)

    if not package_id:
        package_id = create_packaged_component(component_id, package_version, notes)

    package_deployed = query_deployed_package(package_id, environment_id, False)
    if not package_deployed:
        deployment_id = create_deployed_package(release, package_id, environment_id)
        # delete_deployed_package(deployment_id)

    if "schedule" in release:
        conceptual_id = query_process_schedules(atom_id, component_id)
        update_process_schedules(component_id, conceptual_id, atom_id, release["schedule"])
