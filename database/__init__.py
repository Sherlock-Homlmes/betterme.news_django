import os
from dotenv import load_dotenv

load_dotenv()
ENVIRONMENT = os.getenv("ENVIRONMENT")
if ENVIRONMENT == 'local':
    print("You have started local db")
    from .database_port import *
elif ENVIRONMENT == 'docker':
    print("You have started docker db")
    from .docker_database_port import *
