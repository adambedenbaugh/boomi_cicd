import os

from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.environ.get("BOOMI_BASE_URL")
ACCOUNT_ID = os.environ.get("BOOMI_ACCOUNT_ID")
USERNAME = os.environ.get("BOOMI_USERNAME")
PASSWORD = os.environ.get("BOOMI_PASSWORD")
ENVIRONMENT_NAME = os.environ.get("BOOMI_ENVIRONMENT_NAME")
ATOM_NAME = os.environ.get("BOOMI_ATOM_NAME")
ATOM_NAME_DR = os.environ.get("BOOMI_ATOM_NAME_DR")
COMPONENT_GIT_URL = os.environ.get("BOOMI_COMPONENT_GIT_URL")
WORKING_DIRECTORY = os.environ.get("BOOMI_WORKING_DIRECTORY")
CLI_BASE_DIR = os.environ.get("BOOMI_CLI_BASE_DIR", "")
RELEASE_BASE_DIR = os.environ.get("BOOMI_RELEASE_BASE_DIR", "")
RELEASE_FILE = os.environ.get("BOOMI_RELEASE_FILE")

# Set AtomSphere API Rate Limit - 10 calls per second
CALLS = 10
RATE_LIMIT = 1

# Set AtomSphere API XML namespace
NAMESPACES = {"bns": "http://api.platform.boomi.com/"}
