import os

CLI_BASE_DIR = os.environ.get("CLI_BASE_DIR", "")
RELEASE_BASE_DIR = os.environ.get("RELEASE_BASE_DIR", "")

# Set AtomSphere API Rate Limit
CALLS = 10
RATE_LIMIT = 1

# Set AtomSphere API XML namespace
namespaces = {'bns': 'http://api.platform.boomi.com/'}
