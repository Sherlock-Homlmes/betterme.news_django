"""bettermenews URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import re
from django.contrib import admin
from django.urls import path, include, re_path

from .views import (
zzz_admin_page, zzz_oauth, zzz_page_content,zzz_user_page,
zzz_other,
chat,
zzz_test_page
)

urlpatterns = [
##### Testing

    #websocket
    path('video-call',zzz_test_page.video_call),


    ### timer and todolist
    path('todolist/',zzz_user_page.todolist,name="todolist"),
    path('todolist/add-task/<str:task_name>',zzz_user_page.add_todolist,name="add new todo"),
    path('todolist/del-task/<str:task_name>',zzz_user_page.del_todolist,name="del todo"),

    path('timer/',zzz_user_page.timer,name="timer"),
    path('timer/edit/<int:pomodoro_study>/<int:pomodoro_break>',zzz_user_page.timer_edit,name="add new todo"),
    path('timer/section-done/',zzz_user_page.section_done,name="call when section is done"),

##### Real

    ### neccess
    path("robots.txt",zzz_other.robot_txt,name="SEO: robot.txt"),
    path("about-us/",zzz_other.about_us,name="about us"),
    # path("policy/"),
    # path("private/"),
    # path("support/"),
    # path("eco-system/"),

    ### rest api
    path('topic-type/',zzz_page_content.return_topic_type),


    path("404_error/",zzz_page_content.error_404),

    ### login
    path('discord_oauth',zzz_oauth.discord_oauth,name="discord-oauth"),
    path('logout',zzz_oauth.logout,name="discord-logout"),

    ### admin page
    path('admin-page/report',zzz_admin_page.admin_page_report,name="admin analy report"),
    path('admin-page/job',zzz_admin_page.admin_page_job,name="admin job"),
    path('admin-page/team/<str:room_name>',zzz_admin_page.admin_page_team,name="team chat"),
    path('admin-page/team/load-chat/<int:last_message>',zzz_admin_page.load_chat,name="load chat"),

    ### user infomation
    path('account',zzz_user_page.account,name='basic infomation'),
   
    ### page content(always last)
    
    path('', zzz_page_content.home,name="index"),
    path('page-<int:page_number>/',zzz_page_content.page_number,name="page number "),
    path('<str:name>/page-<int:page_number>/',zzz_page_content.topic_page,name="topic page"),
    path('contact-form',zzz_page_content.contact_form),
    path('comment/<str:name>/<int:rate>/<str:comment>/',zzz_page_content.comment,name="comment" ),
    path('search-result/<str:type><str:name>/',zzz_page_content.search_result,name="search result"),
    path('<str:name>/',zzz_page_content.news_post,name="news post"),
    
    ### scraping web
    path('auto-scrap/<int:page_number>',zzz_admin_page.auto_scrap,name="auto-scrap"),
    path('auto-scrap/check-content/<str:name>',zzz_admin_page.scrap_check,name="scrap-check"),
    path('auto-scrap/confirm/',zzz_admin_page.scrap_confirm,name="scrap-check"),
    #path('/auto-scrap/confirm'),
    
]

websocket_urlpatterns = [
    re_path(r'^ws/chat/(?P<room_name>\w+)$',chat.EmployeeChat.as_asgi(),name="chat"),
    #re_path(r'^video-call\w+)$',chat.EmployeeChat.as_asgi(),name="rtc"),
]
