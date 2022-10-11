import imp
from zenora import APIClient

from all_env import TOKEN,CLIENT_SECRET

client = APIClient(TOKEN, client_secret=CLIENT_SECRET)

admin_id = [880359404036317215,278423331026501633]

def get_discord_user(access_token):

  if access_token == None:
    current_user = None

  else:
    try:
      bearer_client = APIClient(access_token, bearer=True)
      current_user = bearer_client.users.get_current_user()
    except Exception as e:
      print(e)
      current_user = None

  return current_user

def is_admin(current_user) -> bool:
  if current_user:
    if current_user.id in admin_id:
      return True
    else:
      return False
  else:
    return False