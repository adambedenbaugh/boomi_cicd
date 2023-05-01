from boomi_cicd.util.environment import *
from boomi_cicd.util.environment_extensions import *

# The environment_extensions_update.py script is used to update the environment extensions for the
# environment set within the environment variables json.


# Open environment variables
# command line: -e
env = set_env()
# Open environment extensions release json
# command line: -r
env_ext_release = set_release()
environment_id = query_environment(env)
update_environment_extensions(env, environment_id, env_ext_release)
