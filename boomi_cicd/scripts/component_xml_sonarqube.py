import os
from zipfile import ZipFile

import requests

import boomi_cicd
from boomi_cicd.util.common_util import set_release, logger

releases = set_release()

base_dir = "cloned_repo"

# TODO: Detect OS
# https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-4.8.0.2856-linux.zip
# https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-4.8.0.2856-windows.zip
# Download SonarQube
url = "https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/"
sonarqube_version = "sonar-scanner-cli-4.8.0.2856-windows"
sonarqube_version_zip = f"{sonarqube_version}.zip"
sonarqube_version_unzip = "sonar-scanner-4.8.0.2856-windows"

# linux= "sonar-scanner-cli-4.8.0.2856-linux.zip"
r = requests.get(url + sonarqube_version + ".zip", allow_redirects=True)
with open(f"{boomi_cicd.CLI_BASE_DIR}/{sonarqube_version_zip}", "wb") as f:
    f.write(r.content)

# Extract SonarQube
with ZipFile(f"{boomi_cicd.CLI_BASE_DIR}/{sonarqube_version_zip}", "r") as zipObj:
    zipObj.extractall(f"{boomi_cicd.CLI_BASE_DIR}")
    zipObj.close()

sonarProjectKey = "test"
logger.info(f"sonarProjectKey: {sonarProjectKey}")
baseFolder = f"C:\\Code\\VSCode\\boomi-cli\\cloned_repo"
logger.info(f"baseFolder: {baseFolder}")
sonarHostURL = "http://localhost:9000"
logger.info(f"sonarHostURL: {sonarHostURL}")
sonarToken = ""  # "admin"
logger.info(os.system("cd"))
os.system(
    fr"{sonarqube_version_unzip}\bin\sonar-scanner.bat"
    fr" -Dsonar.projectKey={sonarProjectKey}"
    fr" -Dsonar.projectBaseDir={baseFolder}"
    fr" -Dsonar.sources={baseFolder}"
    fr" -Dsonar.verbose=true"
    fr" -Dsonar.host.url={sonarHostURL}"
    # f" -Dsonar.login={sonarToken}"
)

"""
# Start SonarQube via Command Line
# https://github.com/OfficialBoomi/boomicicd-cli/blob/master/cli/scripts/bin/sonarScanner.sh
# https://docs.sonarqube.org/latest/analyzing-source-code/scanners/sonarscanner/
 cd "${SONAR_HOME}"/bin
 ./sonar-scanner \
  -Dsonar.projectKey="${sonarProjectKey}" \
  -Dsonar.projectBaseDir="${baseFolder}" \
  -Dsonar.sources="${baseFolder}" \
  -Dsonar.host.url="${sonarHostURL}" \
  -Dsonar.login="${sonarToken}"
"""

# for release in releases["pipelines"]:
#     component_id = release["componentId"]
#     process_name = release["processName"]
#     package_version = release["packageVersion"]
#     process_base_dir = f"{base_dir}/{process_name}"
