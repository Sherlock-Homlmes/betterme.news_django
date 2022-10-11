##### django
from django.http import HttpResponse
from django.shortcuts import redirect

##### 
from .discord_user import (
    #obj
    client,
    #function
    get_discord_user, is_admin
)
from all_env import REDIRECT_URL
from database.mongodb.discord_user import discord_user
from database.redis.discord_user import DiscordUserOauth

async def discord_oauth(request):

    #print(code)
    print(request.GET.get('code'))
    code = request.GET.get('code')

    URIFragments = client.oauth.get_access_token(code, REDIRECT_URL)
    URIFragments.expires_in = None
    discord_access_token = URIFragments.access_token

    current_user = get_discord_user(discord_access_token)
    if current_user:

      discord_user(current_user)

      pre_page = request.COOKIES.get("pre_page")
      print(pre_page)
      resp = redirect(f"/{pre_page}/")
      #resp = HttpRequest("u r login")
      resp.set_cookie(
        key="discord_access_token",
        value=discord_access_token,
        #httponly=True,
        secure= True
        )

      return resp

    else:
      return "Something wrong with your login"

async def logout(request):

  access_token = request.COOKIES.get("discord_access_token")
  if access_token != None:
    pre_page = request.COOKIES.get("pre_page")
    print(pre_page)
    if pre_page:
        response = redirect(f"/{pre_page}")
        response.delete_cookie("discord_access_token")
    else:
        response = redirect("/")
        response.delete_cookie("discord_access_token")        

    return response