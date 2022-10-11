#django
import email
from unicodedata import name
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.template.response import TemplateResponse
#from django.views.decorators.cache import cache_page

import time

import asyncio

from .forms import *
from all_env import OAUTH_URL
### excisting directories
#load page
from .load_page_engine import load_page, load_topic,take_ndb, topic_count,view_process
#database
from database.mongodb.rac import creRAC, takeRAC, take_rate_number_by_pos, check_can_comment
from database.mongodb.user_analyze import analyze_user
from database.redis.post import PostContent
#oauth
from .discord_user import *
from .zzz_oauth import DiscordUserOauth
#models


###############index

topics = ["khoa-hoc","lich-su","dia-ly","sinh-hoc",
         "10-van-cau-hoi-vi-sao","su-that-thu-vi","1001-bi-an","danh-nhan-the-gioi","the-gioi-dong-vat",
         "y-hoc-suc-khoe","kien-truc-doc-dao"]
         
topic_type = {

  "khoa-hoc-han-lam":{
  "name":"Khoa hoc han lam",
  "background_color":"#B5EAD7",
  "fields":{
    "khoa-hoc":{
      'name':'Khoa hoc',
      'image':'khoahoc.webp',
      "background_color":"#00cfde",
    },
    "lich-su":{
      'name':'Lich su',
      'image':'lichsu.webp',
      "background_color":"#ff6961",
    },
    "dia-ly":{
      'name':'Dia ly',
      'image':'dialy.png',
      "background_color":"#c8f3cd",
    },
    "sinh-hoc":{
      'name':'Sinh hoc',
      'image':'sinhhoc.webp',
      "background_color":"#ff7dcb",
    },
  },},

  "nang-tam-hieu-biet":{
  "name":"Nang tam hieu biet",
  "background_color":"#FFB7B2",
  "fields":{
    "10-van-cau-hoi-vi-sao":{
      'name':'10 van cau hoi vi sao',
      'image':'visao.webp',
      "background_color":"#FFDFD3",
    },
    "su-that-thu-vi":{
      'name':'Su that thu vi',
      'image':'suthat.png',
      "background_color":"#74bbfb",
    },
    "1001-bi-an":{
      'name':'1001 bi an',
      'image':'bian.webp',
      "background_color":"#fbb474",
    },
    "danh-nhan-the-gioi":{
      'name':'Danh nhan the gioi',
      'image':'danhnhan.webp',
      "background_color":"#ff5c5c",
    },
    "the-gioi-dong-vat":{
      'name':'The gioi dong vat',
      'image':'dongvat.webp',
      "background_color":"#967bb6",
    },  
  },},


  "kien-thuc-thuc-te":{
  "name":"Kien thuc thuc te",
  "background_color":"#C7CEEA",
  "fields":{
    "y-hoc-suc-khoe":{
      'name':'Y hoc suc khoe',
      'image':'yhoc.webp',
      "background_color":"#000080",
    },
  },},
  #"fields":["y-hoc-suc-khoe","kien-truc-doc-dao"kientrucdocdao.png],
}

topic_type_converter = {"All":""}
for bigkey,bigvalue in topic_type.items():
  for topic in bigvalue["fields"].keys():
    topic_type_converter[bigvalue["fields"][topic]["name"]] = topic

admin_id = [880359404036317215,278423331026501633]

stable_pos = topic_count("count")["value"]
##### done

##### error page
async def error_404(request):
  pre_page = request.COOKIES.get('pre_page')
  if pre_page:
    pre_page = f"/{pre_page}/"
  else:
    pre_page = ""

  response = redirect((pre_page))
  return response
  

##### content
async def home(request):
  return page_number(request,1)

def page_number(request,page_number:int):

  start_time = time.time()

  if page_number > 0:
    tam1, tam2, tam3 = load_page(page_number)

    post_list = tam1
    hot_list = tam2
    hot_first = hot_list[0]
    del hot_list[0]
    most_view_list = tam3

    end_time = time.time()
    print('Total all time elapsed: %.6f seconds' % (end_time - start_time))

    current_user = DiscordUserOauth(request)
    ad_check = is_admin(current_user)
    response = None
    next_page = None

    if len(post_list) >= 17:
      next_page = True

    response = TemplateResponse(request,"news.html",{
      "topic_type": topic_type,

      "post_list":post_list,
      "hot_first":hot_first,
      "hot_list":hot_list,
      "most_view_list":most_view_list,
      "page":page_number,
      "next_page": next_page,

      "current_user": current_user,
      "OAUTH_URL": OAUTH_URL,
      "ad_check":ad_check,

      "form":Contact(),
      })
    
    if response:
      response.set_cookie("pre_page",f"page-{page_number}")
      return response


  return TemplateResponse(request,"404_error.html",{"request":request})

def topic_page(request,name:str,page_number:int):
  global topics
  
  if name in topics:
    post_list,most_view_list = load_topic(name,page_number)

    for bigkey,bigvalue in topic_type.items():
      for key in bigvalue["fields"].keys():
        if key == "y-hoc-suc-khoe":
          name = bigvalue["fields"][key]["name"]
          print(name)

    current_user = DiscordUserOauth(request)
    ad_check = is_admin(current_user)
    next_page = None


    if len(post_list) >= 17:
      next_page = True

    response =  TemplateResponse(request,"topic.html",{
      "topic_type": topic_type,
      
      "topic_name": name,
      "post_list":post_list,
      "most_view_list":most_view_list,
      "page":page_number,
      "next_page":next_page,

      "current_user":current_user,
      "OAUTH_URL": OAUTH_URL,
      "admin":ad_check,
      })

    response.set_cookie("pre_page",f"{name}/page-{page_number}/")
    return response
    
  else:
      print('404 error topic: '+name)
      return TemplateResponse(request,"404_error.html",{"request":request})


def news_post(request,name:str):

  start_time = time.time()
  key = PostContent(name)

  if key != False:
      description = key['description']
      keywords = key['keywords']
      title = key["title"]
      content = key["content"]
      html_type = key["html_type"]

      position = key['position']
      tags = key["tags"]

      if "og_image" in key:
        og_image = key["og_image"]
      else:
        og_image = None

      #take current user
      current_user = DiscordUserOauth(request)

      #take rate and comment (rewrite with ajax)
      rac = takeRAC('position',position)

      if current_user:
        can_cmt = check_can_comment(current_user.id,position)
      else:
        can_cmt = True
      print('Total time post load: %.6f seconds' % (time.time() - start_time))
      # end page load

      start_time = time.time()
      if current_user:
        analyze_user(current_user.id,{"position":position,"tags":tags})

      print('Total time behavior process: %.6f seconds' % (time.time() - start_time))

      #view post data up
      view_process(key)

      resp = TemplateResponse(request, "news_post.html",
        {
        #page content
        "description":description,
        "keywords":keywords,
        "og_image":og_image,
        "content":content,
        "title":title,
        'html_type':html_type,

        'name': name,

        #current user
        'current_user':current_user,
        'OAUTH_URL':OAUTH_URL,

        #rate and comment
        'position': position,
        'rac': rac,
        'can_cmt': can_cmt
        })

      resp.set_cookie(key="pre_page",value=f"{name}")

      return resp

  else:
    print('404 error content')
    return TemplateResponse(request,"404_error.html",{"request":request})

async def comment(request,name:str,rate:int,comment:str):
  current_user = DiscordUserOauth(request)
  if current_user:
    position = take_ndb("name",name)["position"]
    if position:
      #Comment(position=position,user_id=current_user.id,rate=rate,comment=comment).save()
      comment_number = await take_rate_number_by_pos(position)
      await creRAC(current_user.id,position,rate,comment,comment_number)

      return HttpResponse('oke')

async def take_comment(request,name:str):
  pass

async def return_topic_type(request):
  return JsonResponse(topic_type_converter)

async def search_result(request,type:str,name:str):
  current_user = DiscordUserOauth(request)
  return TemplateResponse(request,'',
  {
    'current_user':current_user,
    'type':type,
    'name':name,
  })

async def contact_form(request):
  #await asyncio.sleep(1)
  if request.method == 'POST':
    form = Contact(request.POST)
    #print(form)
    if form.is_valid():
      name = form.cleaned_data['name']
      email = form.cleaned_data['email']
      message = form.cleaned_data['message']
      print(name,email,message)
      return HttpResponse("valid")
    else:
      return HttpResponse("invalid")