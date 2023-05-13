from boomi_cicd.util.common_util import *


def get_package_component_manifest(env, packaged_component_id):
    resource_path = f"/PackagedComponentManifest/{packaged_component_id}"
    logging.info(resource_path)

    response = requests_get_xml(env, resource_path)

    return response.text
