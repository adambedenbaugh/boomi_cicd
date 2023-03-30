
from packaged_component import *
from common_util import *
from atom_query import *
from deployed_package import *
from environment import *
from packaged_component import *
import requests

# Open environment variables 
env = parse_json("local/env.json")
# Open release json
releases = parse_json("local/release.json")

environment_id = query_environment(env)
log("Environment Id")
print(environment_id)

for release in releases["pipelines"]:
    component_id = release["componentId"]
    process_name = release["processName"]
    package_version = release["packageVersion"]

    log("Package Id")
    package_id = query_packaged_component(env, release)

    if not package_id:
        print("Release: {}".format(release))
        package_id = create_packaged_component(env, release)
        print("packageId: {}".format(package_id))

    log("Package Deployed")
    package_deployed = query_deployed_package(env, release, package_id, environment_id)
    if not package_deployed:
        create_deployed_package(env, release, package_id, environment_id)

    