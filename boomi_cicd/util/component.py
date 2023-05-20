from boomi_cicd.util.common_util import *


def query_component(component_id):
    # Create JSON template for connector, dynamic process properties,
    # and process properties.
    resource_path = "/Component/{}".format(component_id)

    response = requests_get_xml(resource_path)

    return response.text
