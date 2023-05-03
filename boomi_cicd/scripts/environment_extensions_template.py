from boomi_cicd.util.component import *
from boomi_cicd.util.environment_extensions import *

# The environment_extensions_template.py script is used to generate a template for environment extensions
# based on the processes within the release json. Once the template is generated and populated, it can be
# used with the environment_extensions_update.py script to update the environment extensions for the
# environment.


# Open environment variables
env = set_env()
# Open release json
# command line: -r
releases = set_release()

connections_dict = []
dpp_dict = []
pp_dict = []
env_template = os.path.join(env["workingDirectory"], "boomi_cicd/util/json/environmentExtensionsTemplate.json")
populated_env_template = parse_json(env_template)

for release in releases["pipelines"]:
    component_id = release["componentId"]
    # process_name = release["processName"]

    response = query_component(env, component_id)
    connections_dict = parse_connection_extensions(connections_dict, response)
    dpp_dict = parse_dpp_extensions(dpp_dict, response)
    pp_dict = parse_pp_extensions(pp_dict, response)

populated_env_template["connections"]["connection"] = connections_dict
populated_env_template["properties"]["property"] = dpp_dict
populated_env_template["processProperties"]["ProcessProperty"] = pp_dict
