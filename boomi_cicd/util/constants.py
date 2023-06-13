import os

from dotenv import load_dotenv

load_dotenv()

# Base URL for Boomi API
BASE_URL = os.environ.get("BOOMI_BASE_URL")
"""Base URL for Boomi AtomSphere API."""
ACCOUNT_ID = os.environ.get("BOOMI_ACCOUNT_ID")
"""Account ID for Boomi AtomSphere API."""
USERNAME = os.environ.get("BOOMI_USERNAME")
"""Username for Boomi AtomSphere API. If using an API Token (recommended), then BOOMI_TOKEN. will prefix the username."""
PASSWORD = os.environ.get("BOOMI_PASSWORD")
"""Password for Boomi AtomSphere API. Often it is an API Token."""
ENVIRONMENT_NAME = os.environ.get("BOOMI_ENVIRONMENT_NAME")
"""Environment Name for deployments."""
ATOM_NAME = os.environ.get("BOOMI_ATOM_NAME")
"""Atom Name for deployments."""
ATOM_NAME_DR = os.environ.get("BOOMI_ATOM_NAME_DR")
"""Atom Name for DR deployments."""
COMPONENT_GIT_URL = os.environ.get("BOOMI_COMPONENT_GIT_URL")
"""Git URL for component. Used when copying component XML to a repository."""
WORKING_DIRECTORY = os.environ.get("BOOMI_WORKING_DIRECTORY")
"""TODO"""
CLI_BASE_DIR = os.environ.get("BOOMI_CLI_BASE_DIR", "")
"""TODO"""
RELEASE_BASE_DIR = os.environ.get("BOOMI_RELEASE_BASE_DIR", "")
"""TODO"""
RELEASE_FILE = os.environ.get("BOOMI_RELEASE_FILE")
"""TODO"""
SONAR_RULES_FILE = os.environ.get(
    "BOOMI_SONAR_RULES_FILE", "boomi_cicd/util/sonarqube/BoomiSonarRules.xml"
)
"""TODO"""

# Set AtomSphere API Rate Limit - 10 calls per second
CALLS = os.environ.get("BOOMI_API_CALLS", 20)
RATE_LIMIT = os.environ.get("BOOMI_API_RATE_LIMIT", 1)
RATE_LIMIT_MILLISECONDS = RATE_LIMIT * 1000

# Set AtomSphere API XML namespace
NAMESPACES = {"bns": "http://api.platform.boomi.com/"}
