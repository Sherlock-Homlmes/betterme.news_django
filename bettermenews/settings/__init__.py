from all_env import ENVIRONMENT

if ENVIRONMENT == 'local':
    print("You have started local page")
    from .local_settings import *
elif ENVIRONMENT == 'docker':
    print("You have started docker page")
    from .docker_settings import *

