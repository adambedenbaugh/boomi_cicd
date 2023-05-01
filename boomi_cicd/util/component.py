import xmltodict

from boomi_cicd.util.common_util import *


def query_component(env, component_id):
    # Create JSON template for connector, dynamic process properties,
    # and process properties.
    resource_path = "/Component/{}".format(component_id)

    response = requests_get_xml(env, resource_path)

    # Convert xml response to json. Remove namespaces and attributes.
    json_response = xmltodict.parse(response.text, attr_prefix='', process_namespaces=False)
    return response.text
