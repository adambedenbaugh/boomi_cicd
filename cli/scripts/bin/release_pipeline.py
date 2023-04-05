from deployed_package import *
from environment import *
from packaged_component import *

# Open environment variables
# command line: -e
env = set_env()
# Open release json
# command line: -r
releases = set_release()

environment_id = query_environment(env)

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
