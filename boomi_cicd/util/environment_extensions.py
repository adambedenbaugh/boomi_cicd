import xml.etree.ElementTree as ET

from boomi_cicd.util.common_util import *
from boomi_cicd.util.component import query_component


# https://help.boomi.com/bundle/developer_apis/page/int-Environment_extensions_object.html


def parse_connection_extensions(connection_array, xml_response):
    """
    Parse the connection extensions from the Component XML response and update the connection array. The connection
    array is used when creating a template for environment extensions updates.

    :param connection_array: The array of connections.
    :type connection_array: list[dict]
    :param xml_response: The XML response containing the connection extensions.
    :type xml_response: str
    :return: The updated connection array.
    :rtype: list[dict]
    """
    root = ET.fromstring(xml_response)
    existing_connection_id = {conn["id"] for conn in connection_array}

    for connection_override in root.findall(
            ".//bns:processOverrides/Overrides/Connections/ConnectionOverride",
            boomi_cicd.NAMESPACES,
    ):
        if connection_override.attrib["id"] not in existing_connection_id:
            new_connection = {
                "id": connection_override.attrib["id"],
                "name": "",  # TODO: query id to get connector name
                "@type": "Connection",
                "field": [],
            }
            connection_array.append(new_connection)

        for conn in connection_array:
            # Look for the connection in the array
            # Add fields to the connection
            if conn["id"] == connection_override.attrib["id"]:
                connection_fields = conn["field"]
                for field in connection_override.findall("field"):
                    if field.attrib["overrideable"] == "true":
                        existing_field = next(
                            (
                                fld
                                for fld in connection_fields
                                if fld["id"] == field.attrib["id"]
                            ),
                            None,
                        )
                        if existing_field is None:
                            new_field_object = {
                                "@type": "field",
                                "id": field.attrib["id"],
                                "lable": field.attrib["label"],
                                "value": "",
                                "usesEncryption": False,
                                "useDefault": False,
                            }
                            connection_fields.append(new_field_object)

    return connection_array


def parse_dpp_extensions(dpp_list, xml_response):
    """
    Parse the DPP (Dynamic Process Property) extensions from the Component XML response and update the DPP list.
    The DPP list is used when creating a template for environment extensions updates.

    :param dpp_list: The list of DPPs.
    :type dpp_list: list[dict]
    :param xml_response: The XML response containing the DPP extensions.
    :type xml_response: str
    :return: The updated DPP list.
    :rtype: list[dict]
    """
    root = ET.fromstring(xml_response)

    for prop_override in root.findall(
            ".//bns:processOverrides/Overrides/Properties/PropertyOverride",
            boomi_cicd.NAMESPACES,
    ):
        existing_dpp = next(
            (dpp for dpp in dpp_list if dpp == prop_override.attrib["name"]), None
        )
        if existing_dpp is None:
            new_dpp = {"@type": "", "name": prop_override.attrib["name"], "value": ""}
            dpp_list.append(new_dpp)

    return dpp_list


def parse_pp_extensions(pp_dict, xml_response):
    """
    Parse the process property extensions from the XML response and update the Process Property dictionary.
    The Process Property dictionary is used when creating a template for environment extensions updates.

    :param pp_dict: The dictionary of process properties.
    :type pp_dict: list[dict]
    :param xml_response: The XML response containing the process property extensions.
    :type xml_response: str
    :return: The updated process property dictionary.
    :rtype: list[dict]
    """
    root = ET.fromstring(xml_response)
    for process_prop_override in root.findall(
            ".//bns:processOverrides/Overrides/DefinedProcessPropertyOverrides/OverrideableDefinedProcessPropertyComponent",
            boomi_cicd.NAMESPACES,
    ):
        existing_pp_ids = {pp["id"] for pp in pp_dict}
        if process_prop_override.attrib["componentId"] not in existing_pp_ids:
            new_pp = {
                "id": process_prop_override.attrib["componentId"],
                "name": "",  # TODO: query id to get connector name
                "@type": "OverrideProcessProperty",
                "ProcessPropertyValue": [],
            }
            pp_dict.append(new_pp)

        for pp in pp_dict:
            # Look for the process property ids in the array
            # Add fields to the process property array
            if pp["id"] == process_prop_override.attrib["componentId"]:
                pp_values = pp["ProcessPropertyValue"]
                for overide_pp_vaule in process_prop_override.findall(
                        "./OverrideableDefinedProcessPropertyValue"
                ):
                    if overide_pp_vaule.attrib["overrideable"] == "true":
                        existing_pp_value = next(
                            (
                                pp_value
                                for pp_value in pp_values
                                if pp_value["key"] == overide_pp_vaule.attrib["key"]
                            ),
                            None,
                        )
                        if existing_pp_value is None:
                            new_pp_value = {
                                "@type": "ProcessPropertyValue",
                                "label": overide_pp_vaule.attrib["name"],
                                "key": overide_pp_vaule.attrib["key"],
                                "value": "",
                                "encryptedValueSet": False,
                                "useDefault": False,
                            }
                            pp_values.append(new_pp_value)

    return pp_dict


def parse_cross_reference_extensions(cross_reference, xml_response):
    """
    Parse the cross-reference extensions from the Component XML response and update the cross-reference list.
    The cross-reference list is used when creating a template for environment extensions updates.

    :param cross_reference: The list of cross-references.
    :type cross_reference: list[dict]
    :param xml_response: The XML response containing the cross-reference extensions.
    :type xml_response: str
    :return: The updated cross-reference list.
    :rtype: list[dict]
    """
    root = ET.fromstring(xml_response)
    cr_ids = {cr["id"] for cr in cross_reference}
    for cross_reference_override in root.findall(
            ".//bns:processOverrides/Overrides/CrossReferenceOverrides/CrossReferenceOverride",
            boomi_cicd.NAMESPACES,
    ):
        if cross_reference_override.attrib["id"] not in cr_ids:
            new_cross_reference = {
                "@type": "CrossReference",
                "CrossReferenceRows": {"@type": "", "row": []},
                "id": cross_reference_override.attrib["id"],
                "overrideValues": True,
                "name": cross_reference_override.attrib["name"],
            }

            cross_reference_xml = query_component(cross_reference_override.attrib["id"])
            cross_reference_root = ET.fromstring(cross_reference_xml)
            for cross_reference_rows in cross_reference_root.findall(
                    ".//bns:object/CrossRefTable/Rows/row", boomi_cicd.NAMESPACES
            ):
                new_row = {"@type": "CrossReferenceRow"}
                for cross_reference_col in cross_reference_rows.findall(".//ref"):
                    col_index = int(cross_reference_col.attrib["colIdx"]) + 1
                    new_row["ref" + str(col_index)] = cross_reference_col.attrib[
                        "value"
                    ]
                new_cross_reference["CrossReferenceRows"]["row"].append(new_row)

            cross_reference.append(new_cross_reference)

    return cross_reference


def get_environment_extensions(environment_id):
    """
    Get the extensions for the specified environment.

    :param environment_id: The ID of the environment.
    :type environment_id: str
    :return: The environment extensions.
    :rtype: dict
    """
    resource_path = "/EnvironmentExtensions/{}".format(environment_id)
    response = requests_get(resource_path)

    return json.loads(response.text)


def update_environment_extensions(environment_id, payload):
    resource_path = "/EnvironmentExtensions/{}/update}".format(environment_id)
    response = requests_post(resource_path, payload)

    return json.loads(response.text)
