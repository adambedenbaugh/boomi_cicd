from boomi_cicd.util.common_util import *


def query_component(component_id):
    """
    Query a component by its ID.

    This function queries a component in Boomi by its ID and retrieves the corresponding information.
    The component ID is used to construct the resource path for the API request.
    The response is returned as the XML text of the component.

    :param component_id: The ID of the component to query.
    :return: The XML text of the component.
    """
    resource_path = "/Component/{}".format(component_id)

    response = requests_get_xml(resource_path)

    return response.text
