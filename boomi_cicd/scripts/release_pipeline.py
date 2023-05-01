from boomi_cicd.util.atom import query_atom
from boomi_cicd.util.deployed_package import *
from boomi_cicd.util.environment import *
from boomi_cicd.util.packaged_component import *
from boomi_cicd.util.process_schedules import update_process_schedules, query_process_schedules

# print(os.getcwd())
# Open environment variables
# command line: -e
env = set_env()
# Open release json
# command line: -r
releases = set_release()

environment_id = query_environment(env)
atom_id = query_atom(env, env["atomName"])

for release in releases["pipelines"]:
    component_id = release["componentId"]
    process_name = release["processName"]
    package_version = release["packageVersion"]

    package_id = query_packaged_component(env, release)

    if not package_id:
        package_id = create_packaged_component(env, release)

    package_deployed = query_deployed_package(env, release, package_id, environment_id)
    if not package_deployed:
        deployment_id = create_deployed_package(env, release, package_id, environment_id)
        # delete_deployed_package(env, deployment_id)

    if "schedule" in release:
        conceptual_id = query_process_schedules(env, atom_id, component_id)
        update_process_schedules(env, component_id, conceptual_id, atom_id, release["schedule"])
