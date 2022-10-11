from threading import Thread
import os
from other_modules.decorators import count_run_time
######database
from ..main import dtb,tdtb,ldtb

from ...meilisearch.news import news_index,add_news_meili
from ...redis.post import MultiMinimumPost



#start
#########################################database#####################################
#cre_data
def ndb(value):

  tag_count = topic_count("count")
  tag_count["value"] += 1
  pos = tag_count["value"]
  value['position'] = pos
  update_topic_count("count",tag_count)
  
  for key in value["tags"]:
    topic = topic_count(key)
    topic["value"] += 1
    topic["position"].insert(0,pos)
    update_topic_count(key,topic)

  #insert multi database
  dtb.insert_one(value)
  minimum_data(value)
  #add_news_meili(value)


def minimum_data(element:dict):
  ele = {}
  ele["position"] = element["position"]
  ele["name"] = element["name"]
  ele["title"] = element["title"]
  ele["description"] = element["description"]
  ele["slide_show_link"] = element["slide_show_link"]
  ele["thumbnail_link"] = element["thumbnail_link"]

  ldtb.insert_one(ele)
  print(" ")
  print("insert minimum element done")
  print(ele)
  print(" ")


#take_data
def take_ndb(key,value):
  tests = dtb.find_one( { '{}'.format(key): value } )
  if tests:
    return tests 
  else: 
    return False

#update_data
def update_ndb(pos,value):
  global dtb
  dtb.update_one({ 'position': pos },  {'$set':value} )

#count

def topic_count(key:str):
  tests = tdtb.find_one( { 'name': key } )
  return tests

def update_topic_count(key,value):
  tdtb.update_one({"name":key},{'$set':value})

#update element
def update_element(pos:int,key:str,value):
  dtb.update_one({"position":pos},{'$set':{'{}'.format(key) : value }})

################################################### page process
#tag find
def position_show(pos_start:int,pos_end:int):
  element = dtb.find({ 'position': {'$gt':pos_start-1,'$lt':pos_end+1} }).sort('position',-1)

  value = []
  for ele in element:
    value.append(ele)

  return value

#find element in post list
@count_run_time
def find_pos(pos_list:list):
  value = []
  #print("before post list:"+ str(pos_list))
  pos_list = list(dict.fromkeys(pos_list))
  pos_list, value = MultiMinimumPost(pos_list)
  #print("after post list:"+ str(pos_list))
  if pos_list != []:
    element = ldtb.find({"position": { '$in': pos_list }  })
    for ele in element:
      value.append(ele)

  MultiMinimumPost.set_multi_minimum_post(value)
  return value

##################3 sync with meili
'''
#sync data with mongodb
'''
def sync_meili_mongo():
  elements = dtb.find()
  for element in elements:
    ele = None
    ele = {}
    ele["id"] = element["position"]
    ele["name"] = element["name"]
    ele["title"] = element["title"]
    ele["description"] = element["description"]
    ele["thumbnail_link"] = element["thumbnail_link"]
    ele["tags"] = element["tags"],

    news_index.add_documents(ele)

#sync_meili_mongo()






