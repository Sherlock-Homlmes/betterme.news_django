from .zzz_oauth import (
    #class
    DiscordUserOauth
)
from .discord_user import is_admin
from .auto_scrap import *

#lib
import json,io
from all_env import OAUTH_URL

#django
from django.http import HttpResponse, JsonResponse
from django.template.response import TemplateResponse

from database.mongodb.user_analyze import take_analyze_user,ana_db
from database.meilisearch.chat import employee_chat_index
from database.connector.mongo_meili_chat import full_chat_data

from .zzz_page_content import topic_type

#admin scrap page
async def auto_scrap( request,  page_number: int):
  current_user = DiscordUserOauth(request)
  ad_check = is_admin(current_user)
  print('call auto scrap')
  if ad_check == True:

      #return scrap_by_page_number(page_number)
      scraping = scrap_by_page_number(page_number)
      return TemplateResponse(request,"auto-scrap.html",{
        "scraping": scraping,
        "topics": topic
        })

  else:
    content =  f"""
    <html>
      <a href={OAUTH_URL}>dang nhap</a>
    </html>
    """

    response = HttpResponse(content)
    response.set_cookie(key="pre_page",value=f"auto-scrap/{page_number}")

    return response

async def scrap_check(request,name: str,
  #html_type: str = Form(...),
  #tags: list = Form(...)
  ):

  with open('main/views/check_data.json', encoding='utf-8') as f1:
    all_post = json.load(f1)

  name = "/"+name
  url = "https://khoahoc.tv" + name
  thumbnail_link = all_post[name]['thumb_src']
  name = title_process(name)
  

  data = await test_create_data(url,name,"normal",thumbnail_link,"","",['khoa-hoc'])
  #print(data)

  description = data["description"]
  keywords = data["keywords"]
  html_type = data["html_type"]
  content = data["content"]

  
  return TemplateResponse(request, "demo_news_post.html",
    {
    "description": description,
    "keywords": keywords,
    "html_type": html_type,
    "content": content
    })

async def scrap_confirm(request):

  if request.method == "POST":

    check_list = request.POST.getlist('check_list')
    html_type = request.POST.getlist('html_type')
    tags = request.POST.getlist('tags')

    if 'add-one' in request.POST:
      if request.POST['add-one'] in check_list:
        print(check_list)
        print(html_type)
        print(tags)

        await auto_scrap_process(check_list,html_type,tags)

    elif 'add-all' in request.POST:
      
      check_list = request.POST.getlist('check_list')
      print(check_list)
      print(html_type)
      print(tags)

      await auto_scrap_process(check_list,html_type,tags)

    return HttpResponse("done")


#admin analyze page
async def admin_page_report(request):
  current_user = DiscordUserOauth(request)
  if is_admin(current_user) == True:
    user_data = take_analyze_user("admin")
    
    topic_color = {}
    for bigtopic,bigvalue in topic_type.items():
        for topic,value in bigvalue["fields"].items():
            topic_color[topic] = {}
            topic_color[topic]["name"] =  value["name"]
            topic_color[topic]["background_color"] =  value["background_color"]


    return TemplateResponse(request,"admin-page-report.html",{
        "current_user":current_user,
        "user_data":user_data,
        "topic_color":topic_color,
    })

  else:
    return HttpResponse("get out of here")

#admin chat
async def admin_page_team(request,room_name):
  current_user = DiscordUserOauth(request)
  if current_user:
    last_message = employee_chat_index.get_stats()["numberOfDocuments"] + 1

    return TemplateResponse(request,'discord_chatbox.html',
    {
      "room_name":room_name,
      "current_user":current_user,
      "last_message":last_message,
    })

async def load_chat(request,last_message:int):
  await asyncio.sleep(1)
  current_user = DiscordUserOauth(request)
  if is_admin(current_user) == True:
    data = full_chat_data(last_message)
    return JsonResponse(data)

# admin job apply
async def admin_page_job(request):
  current_user = DiscordUserOauth(request)
  if is_admin(current_user) == True:

    return TemplateResponse(request,"admin-page-job.html",{
        "current_user":current_user,
    })

  else:
    return HttpResponse("get out of here")
