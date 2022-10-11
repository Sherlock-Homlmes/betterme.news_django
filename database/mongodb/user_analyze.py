import datetime
import pytz

######database
from .main import ana_db

topic = ["khoa-hoc","lich-su","dia-ly","sinh-hoc",
         "10-van-cau-hoi-vi-sao","su-that-thu-vi","1001-bi-an","danh-nhan-the-gioi","the-gioi-dong-vat",
         "y-hoc-suc-khoe","kien-truc-doc-dao"]

#start
#########################################database#####################################
#cre_data
def analyze_user(user_id:int,post_data:dict):
    user_view_data = take_analyze_user(user_id)
    if take_analyze_user(user_id) == None:
        print("new analyze user")
        user_view_data = {
            "user_id": user_id,
            "total_views": 0,
            "views_history":[],
            "views_by_pos":{},
            "views_by_tags":{},
            "date_views_history":{}
        }

        ana_db.insert_one(user_view_data)
    
    admin_view_data = ana_db.find_one({ 'user_id': "admin" })
    update_analyze_user(user_view_data,post_data,admin_view_data)

#take_data
def take_analyze_user(user_id) -> list:
  element = ana_db.find_one( { 'user_id': user_id } )

  if element:
    return element
  else:
    return None

#update

def if_in_dict(value1:dict,value2:str):
    if value2 in value1.keys():
        value1[value2] += 1
    else:
        value1[value2] = 1
    return value1
def if_in_list(value1:list,value2:str):
    if value2 in value1:
        value1.remove(value2)
    value1.insert(0,value2)
    return value1

def update_analyze_user(user_view_data,post_data,admin_view_data):
    post_data_example = {
        "position":15,
        "tags":[]
    }

    position = post_data["position"]
    tags = post_data["tags"]
    utc_now = pytz.utc.localize(datetime.datetime.utcnow())
    pst_now = utc_now.astimezone(pytz.timezone("Asia/Ho_Chi_Minh"))
    date = f"{pst_now.year}/{pst_now.month}/{pst_now.day}"

    if date in user_view_data["date_views_history"]:
        user_view_data["date_views_history"][date]["views"] += 1
        admin_view_data["date_views_history"][date]["views"] += 1
        user_view_data["date_views_history"][date]["views_history"] = if_in_list(user_view_data["date_views_history"][date]["views_history"],position)
    else:
        views_by_tags = None
        views_by_tags = {}
        for tag in tags:
            views_by_tags[tag] = 0
        user_view_data["date_views_history"][date] = {
            "views": 1,
            "views_history":[position],
            "views_by_pos":{str(position):0},
            "views_by_tags":views_by_tags,
        }
        if date in admin_view_data["date_views_history"]:
            admin_view_data["date_views_history"][date]["views"] += 1
        else:
            views_by_tags = None
            views_by_tags = {}
            for tag in tags:
                views_by_tags[tag] = 0
            admin_view_data["date_views_history"][date] = {
                "views": 1,
                "views_by_pos":{str(position):0},
                "views_by_tags":views_by_tags,         
            }

    user_view_data["total_views"] += 1
    admin_view_data["total_views"] += 1

    user_view_data["views_history"] = if_in_list(user_view_data["views_history"],position)

    for tag in tags:
        user_view_data["views_by_tags"] = if_in_dict(user_view_data["views_by_tags"],tag)
        user_view_data["date_views_history"][date]["views_by_tags"] = if_in_dict(user_view_data["date_views_history"][date]["views_by_tags"],tag) 
        admin_view_data["views_by_tags"] = if_in_dict(admin_view_data["views_by_tags"],tag)
        admin_view_data["date_views_history"][date]["views_by_tags"] = if_in_dict(admin_view_data["date_views_history"][date]["views_by_tags"],tag)     

    user_view_data["views_by_pos"] = if_in_dict(user_view_data["views_by_pos"],str(position))
    user_view_data["date_views_history"][date]["views_by_pos"] = if_in_dict(user_view_data["date_views_history"][date]["views_by_pos"],str(position))
    admin_view_data["views_by_pos"] = if_in_dict(admin_view_data["views_by_pos"],str(position))
    admin_view_data["date_views_history"][date]["views_by_pos"] = if_in_dict(admin_view_data["date_views_history"][date]["views_by_pos"],str(position))

    ana_db.update_one( { 'user_id': user_view_data["user_id"] },{'$set': user_view_data} )
    ana_db.update_one( { 'user_id': "admin" },{'$set': admin_view_data} )


user_view_data_example ={
    "user_id": 100,
    "total_views": 5,
    "views_history":[35,25],
    "views_by_pos":{},
    "views_by_tags":{},
    "date_view_history":{
        "2022-07-08":{
            "views": 5,
            "post_see":[35,25],
            "views_by_pos":{},
            "views_by_tags":{}
        }
    }
}
admin_view_data_example ={
    "user_id": "admin",
    "total_views": 0,
    "views_by_tags":{},
    "views_by_pos":{},
    "date_view_history":{
        #"2022-07-08":{
        #    "views": 0,
        #    "views_by_tags":{},
        #    "views_by_pos":{}
        #}
    }
}

