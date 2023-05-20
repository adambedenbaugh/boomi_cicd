from boomi_cicd.util.common_util import set_release
from boomi_cicd.util.environment import query_environment
from boomi_cicd.util.environment_extensions import update_environment_extensions

# The environment_extensions_update.py script is used to update the environment extensions for the
# environment set within the environment variables json.


# Open environment extensions release json
env_ext_release = set_release()
environment_id = query_environment()
update_environment_extensions(environment_id, env_ext_release)
