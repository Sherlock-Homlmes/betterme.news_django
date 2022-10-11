import os
from dotenv import load_dotenv
load_dotenv()

#discord
TOKEN = os.getenv("TOKEN")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URL = os.getenv("REDIRECT_URL")
OAUTH_URL = os.getenv("OAUTH_URL")
ENVIRONMENT = os.getenv("ENVIRONMENT")

#google
GG_CLIENT_ID = os.getenv("GG_CLIENT_ID")
GG_CLIENT_SECRET = os.getenv("GG_CLIENT_SECRET")
GG_REDIRECT_URL = os.getenv("GG_REDIRECT_URL")

#facebook


