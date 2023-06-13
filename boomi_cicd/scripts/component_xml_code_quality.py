from lxml import etree

from boomi_cicd.util.common_util import *

# Set report variables
REPORT_TITLE = "Packaged Components Code Quality Report"
REPORT_HEADERS = [
    "#",
    "Component Name",
    "Component ID",
    "Version",
    "Type",
    "Issue",
    "Issue Type",
    "Priority",
]


def print_report_head():
    f.write("# " + REPORT_TITLE + "\n")
    f.write("|" + "|".join(REPORT_HEADERS) + "|\n")
    f.write("|" + "|".join(["---"] * len(REPORT_HEADERS)) + "|\n")


def print_report_row(row_local):
    f.write("|" + "|".join(row_local) + "|\n")


# Open file for report.
# component_xml_git.py clones the repo to a folder called cloned_repo
base_folder = "cloned_repo"
f = open(f"{base_folder}/report.md", "w")

sonar_rules = etree.parse(boomi_cicd.SONAR_RULES_FILE)

print_report_head()
rules_count = len(sonar_rules.xpath("/profile/rules/rule"))
h = 0
for root, _, filenames in os.walk(base_folder):
    for filename in filenames:
        if filename.endswith(".xml"):
            component_file = os.path.join(root, filename)
            component_tree = etree.parse(component_file)
            component_root = component_tree.getroot()
            component_id = component_root.attrib["componentId"]
            component_name = component_root.attrib["name"]
            component_version = component_root.attrib["version"]
            component_type = component_root.attrib["type"]

            for i in range(1, rules_count + 1):
                xpath = f"/profile/rules/rule[{i}]/parameters/parameter[key='expression']/value"
                expressions = sonar_rules.xpath(xpath)

                for expression in expressions:
                    component_validation = component_tree.xpath(
                        expression.text, namespaces=boomi_cicd.NAMESPACES
                    )
                    if component_validation:
                        export_violations_found = True
                        v_priority = sonar_rules.xpath(
                            f"/profile/rules/rule[{i}]/priority/text()"
                        )[0]
                        v_type = sonar_rules.xpath(
                            f"/profile/rules/rule[{i}]/type/text()"
                        )[0]
                        v_name = sonar_rules.xpath(
                            f"/profile/rules/rule[{i}]/description/text()"
                        )[0]
                        h += 1
                        # TODO: Make Component Name a link to the component XML in the report
                        row = [
                            str(h),
                            f"[{component_name}]({component_file})",
                            component_id,
                            component_version,
                            str(component_type),
                            str(v_name),
                            str(v_type),
                            str(v_priority),
                        ]
                        print_report_row(row)

f.close()
