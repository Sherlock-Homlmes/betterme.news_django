from .zzz_oauth import is_admin
from .zzz_page_content import topic_type
from .auto_scrap import *

from all_env import OAUTH_URL
#django
from django.http import HttpResponse
from django.template.response import TemplateResponse

#database
from database.mongodb.timer_todolist import *
from database.mongodb.user_analyze import take_analyze_user
from .zzz_oauth import DiscordUserOauth

#################### start
async def todolist(request):

    current_user = DiscordUserOauth(request)
    if current_user:
        data = take_todo_timer(current_user.id)
        return TemplateResponse(request,"todolist.html",{"data":data})
    else:      
        content =  f"""
        <html>
        <a href={OAUTH_URL}>dang nhap</a>
        </html>
        """

        response = HttpResponse(content)
        response.set_cookie(key="pre_page",value=f"todolist")

        return response 

async def add_todolist(request,task_name:str):
    current_user = DiscordUserOauth(request)
    if current_user:
        new_todo(current_user.id,task_name)
    return HttpResponse("Done")

async def del_todolist(request,task_name:str):
    current_user = DiscordUserOauth(request)
    if current_user:
        del_todo(current_user.id,task_name)
    return HttpResponse("Done")

#################### start
async def timer(request):

    current_user = DiscordUserOauth(request)
    if current_user:
        data = take_todo_timer(current_user.id)
        return TemplateResponse(request,"timer.html",{"data":data})
    else:      
        content =  f"""
        <html>
        <a href={OAUTH_URL}>dang nhap</a>
        </html>
        """

        response = HttpResponse(content)
        response.set_cookie(key="pre_page",value=f"timer")

        return response 

async def timer_edit(request,pomodoro_study:int,pomodoro_break:int):
    current_user = DiscordUserOauth(request)
    if current_user:
        pomodoro_timer(current_user.id,pomodoro_study,pomodoro_break)
    return HttpResponse("Done")
    
async def section_done(request):
    current_user = DiscordUserOauth(request)
    if current_user:
        add_timer(current_user.id)
    return HttpResponse("Done")

###### start
async def account(request):
    current_user = DiscordUserOauth(request)
    user_data = take_analyze_user(current_user.id)

    topic_color = {}

    for bigtopic, bigvalue in topic_type.items():
        for topic,value in bigvalue["fields"].items():
            topic_color[topic] = {}
            topic_color[topic]["name"] =  value["name"]
            topic_color[topic]["background_color"] =  value["background_color"]


    return TemplateResponse(request,"account.html",{
        "current_user":current_user,
        "user_data":user_data,
        "topic_color":topic_color,
    })