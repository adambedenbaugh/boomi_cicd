import datetime
import xml.etree.ElementTree as ET
from os import walk
from xml.dom import minidom

from git import Repo

from boomi_cicd.util.component import query_component
from boomi_cicd.util.component_xml import get_file_refs, set_file_refs
from boomi_cicd.util.package_component_manifest import get_package_component_manifest
from boomi_cicd.util.packaged_component import *

# Open release json
releases = set_release()

base_dir = "cloned_repo"
# Clone repo
cloned_repo = Repo.clone_from(boomi_cicd.COMPONENT_GIT_URL, "cloned_repo")
# cloned_repo = Repo("cloned_repo")

logger.info(f"Git Repo Status: {cloned_repo.git.status()}".replace("\n", " "))

file_components = get_file_refs(base_dir)

for release in releases["pipelines"]:
    component_id = release["componentId"]
    process_name = release["processName"]
    package_version = release["packageVersion"]
    process_base_dir = f"{base_dir}/{process_name}"

    # Check if the packaged component's name has changed. If so, rename the folder
    # Name within the release file is used as the folder name.
    if (
            component_id in file_components
            and process_name != file_components[component_id]
    ):
        logger.info(
            f"Process name changed. Original: {file_components[component_id]}. New: {process_name}"
        )
        cloned_repo.git.mv(f"{file_components[component_id]}", f"{process_name}")
        file_components[component_id] = process_name

    component_refs = {}
    # Check if component id exists in packaged component's .componentRef
    if os.path.exists(process_base_dir):
        component_refs = get_file_refs(process_base_dir)
        logger.info(f"Created component_refs: {component_refs}")

    # Parse xml for component id
    packaged_component_id = query_packaged_component(release)
    packaged_manifest = get_package_component_manifest(packaged_component_id)
    root = ET.fromstring(packaged_manifest)
    component_info_names = set()
    for component_info in root.findall(".//bns:componentInfo", boomi_cicd.NAMESPACES):
        component_info_id = component_info.attrib["id"]

        # Query components
        # TODO: Update query_component to accept version.
        component_xml = query_component(component_info_id)

        # Use the dict to know if a file should be updated or created.
        # Get the component name for the file name
        component_name = ET.fromstring(component_xml).attrib["name"]
        component_file_name = f"{component_name}.xml"
        component_info_names.add(component_file_name)

        if (
                component_info_id in component_refs
                and component_file_name != component_refs[component_info_id]
        ):
            # Check if file needs to be renamed
            logger.info(
                f"Component name changed. Original: {component_refs[component_info_id]}. New: {component_name}"
            )
            cloned_repo.git.mv(
                f"{process_name}/{component_refs[component_info_id]}",
                f"{process_name}/{component_file_name}",
            )

        # Write component xml to file
        with open(f"{process_base_dir}/{component_file_name}", "w") as f:
            f.write(minidom.parseString(component_xml).toprettyxml(indent="  "))

        component_refs[component_info_id] = component_file_name

    # Delete files that are not in the component manifest and romove from component_refs of the packaged component
    for dirpath, dirnames, filenames in walk(process_base_dir):
        for filename in filenames:
            if filename not in component_info_names and filename != ".componentRef":
                cloned_repo.git.rm(f"{process_name}/{filename}")
                logger.info(f"Deleted {filename} from {process_name}")

    set_file_refs(process_base_dir, component_refs)

# Commit all changes
cloned_repo.index.add("*")
commit_message = "Commit from Boomi CICD on {}".format(
    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
)
logger.info(f"Commiting changes: {commit_message}")
cloned_repo.index.commit(commit_message)
cloned_repo.remote('origin').push('main')

set_file_refs("cloned_repo", file_components)
