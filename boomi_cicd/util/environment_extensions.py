import xml.etree.ElementTree as ET

from boomi_cicd.util.common_util import *

# https://help.boomi.com/bundle/developer_apis/page/int-Environment_extensions_object.html

namespaces = {'bns': 'http://api.platform.boomi.com/'}  # namespaces for xml parsing


def parse_connection_extensions(connection_array, xml_response):
    # Parse connector from json response
    # ConnectionOverride can be an object or an array of objects
    # TODO: Consider using xml directly instead of converting to json
    root = ET.fromstring(xml_response)

    for connection_override in root.findall(".//bns:processOverrides/Overrides/Connections/ConnectionOverride",
                                            namespaces):
        existing_connection = next(
            (conn for conn in connection_array if conn["id"] == connection_override.attrib["id"]), None)

        if existing_connection is None:
            new_connection = {
                "id": connection_override.attrib["id"],
                "name": "",  # TODO: query id to get connector name
                "@type": "Connection",
                "field": []
            }
            connection_array.append(new_connection)

        for conn in connection_array:
            # Look for the connection in the array
            # Add fields to the connection
            # TODO: Stopped here
            if conn["id"] == connection_override.attrib["id"]:
                print("hi")
                connection_fields = conn["field"]
                for field in connection_override.findall("field"):
                    if field.attrib["overrideable"] == "true":
                        existing_field = next((fld for fld in connection_fields if fld["id"] == field.attrib["id"]),
                                              None)
                        if existing_field is None:
                            new_field_object = {
                                "@type": "field",
                                "id": field.attrib["id"],
                                "lable": field.attrib["label"],
                                "value": "",
                                "usesEncryption": False,
                                "useDefault": False
                            }
                            connection_fields.append(new_field_object)

    return connection_array


def parse_dpp_extensions(dpp_list, xml_response):
    root = ET.fromstring(xml_response)

    for prop_override in root.findall(".//bns:processOverrides/Overrides/Properties/PropertyOverride", namespaces):
        existing_dpp = next((dpp for dpp in dpp_list if dpp == prop_override.attrib["name"]), None)
        if existing_dpp is None:
            new_dpp = {
                "@type": "",
                "name": prop_override.attrib["name"],
                "value": ""
            }
            dpp_list.append(new_dpp)

    return dpp_list


def parse_pp_extensions(pp_dict, xml_response):
    root = ET.fromstring(xml_response)
    for process_prop_override in root.findall(
            ".//bns:processOverrides/Overrides/DefinedProcessPropertyOverrides/OverrideableDefinedProcessPropertyComponent",
            namespaces):
        existing_pp = next((pp for pp in pp_dict if pp["id"] == process_prop_override.attrib["componentId"]), None)
        if existing_pp is None:
            new_pp = {
                "id": process_prop_override.attrib["componentId"],
                "name": "",  # TODO: query id to get connector name
                "@type": "OverrideProcessProperty",
                "ProcessPropertyValue": []
            }
            pp_dict.append(new_pp)

        for pp in pp_dict:
            # Look for the process property ids in the array
            # Add fields to the process property array
            if pp["id"] == process_prop_override.attrib["componentId"]:
                pp_values = pp["ProcessPropertyValue"]
                for overide_pp_vaule in process_prop_override.findall("./OverrideableDefinedProcessPropertyValue"):
                    if overide_pp_vaule.attrib["overrideable"] == "true":
                        existing_pp_value = next(
                            (pp_value for pp_value in pp_values if pp_value["key"] == overide_pp_vaule.attrib["key"]),
                            None)
                        if existing_pp_value is None:
                            new_pp_value = {
                                "@type": "ProcessPropertyValue",
                                "label": overide_pp_vaule.attrib["name"],
                                "key": overide_pp_vaule.attrib["key"],
                                "value": "",
                                "encryptedValueSet": False,
                                "useDefault": False
                            }
                            pp_values.append(new_pp_value)

    return pp_dict


# "processProperties": {
#                 "@type": "OverrideProcessProperties",
#                 "ProcessProperty": [
#                     {
#                         "@type": "OverrideProcessProperty",
#                         "ProcessPropertyValue": [
#                             {
#                                 "@type": "ProcessPropertyValue",
#                                 "label": "Process Property #1",
#                                 "key": "f056e8a0-cab0-4cc6-bc11-59deba9aca50",
#                                 "value": "",
#                                 "encryptedValueSet": false,
#                                 "useDefault": true
#                             }
#                         ],
#                         "id": "4ffd1564-c1d0-4e45-bd8d-3a2e6bc44850",
#                         "name": "sleep"
#                     }
#                 ]
#             },

def get_environment_extensions(env, environment_id):
    resource_path = "/EnvironmentExtensions/{}".format(environment_id)
    response = requests_get(env, resource_path)
    return json.loads(response.text)


def update_environment_extensions(env: dict, environment_id: str, payload: dict):
    resource_path = "/EnvironmentExtensions/{}/update}".format(environment_id)

    # environment_query = os.path.join(env["workingDirectory"], "boomi_cicd/util/json/atomQuery.json")
    #
    # payload = parse_json(environment_query)
    response = requests_post(env, resource_path, payload)

    return json.loads(response.text)
