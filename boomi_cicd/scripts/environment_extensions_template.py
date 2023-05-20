from boomi_cicd.util.environment_extensions import *

# The environment_extensions_template.py script is used to generate a template for environment extensions
# based on the processes within the release json. Once the template is generated and populated, it can be
# used with the environment_extensions_update.py script to update the environment extensions for the
# environment. It currently supports creating a template for connections, process properties,
# dynamic process properties, and a cross-reference table.


# Open release json
releases = set_release()

connections_dict = []
dpp_dict = []
pp_dict = []
cross_reference_dict = []
env_template = os.path.join(boomi_cicd.WORKING_DIRECTORY, "boomi_cicd/util/json/environmentExtensionsTemplate.json")
populated_env_template = parse_json(env_template)

for release in releases["pipelines"]:
    component_id = release["componentId"]

    response = query_component(component_id)
    connections_dict = parse_connection_extensions(connections_dict, response)
    dpp_dict = parse_dpp_extensions(dpp_dict, response)
    pp_dict = parse_pp_extensions(pp_dict, response)
    cross_reference_dict = parse_cross_reference_extensions(cross_reference_dict, response)

print("=======================================")
populated_env_template["connections"]["connection"] = connections_dict
populated_env_template["properties"]["property"] = dpp_dict
populated_env_template["processProperties"]["ProcessProperty"] = pp_dict
populated_env_template["crossReferences"]["crossReference"] = cross_reference_dict

print(json.dumps(populated_env_template))
