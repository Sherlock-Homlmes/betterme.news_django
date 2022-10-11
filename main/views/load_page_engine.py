import imp
import os
import time
######database
from database.mongodb.news.news_database import (
  #topic_count,
  update_topic_count,
  take_ndb,update_ndb,
  find_pos
)
## thuộc tính: account, password, key1, key2
from database.mongodb.main import dtbs
from database.redis.post import topic_count

dtb = dtbs['news_data']
tdtb = dtbs["topic_position"]
ldtb = dtbs["load_news_data"]

#start
#########################################database#####################################
#update element
def update_element(pos:int,key:str,value):
  dtb.update_one({"position":pos},{'$set':{'{}'.format(key) : value }})

######################## process each content
#view process
def view_process(value):
  pos = value["position"]
  view = value["view"] + 1 
  update_element(pos,"view",view)

  tags = value["tags"]
  tags.append("count")

  for tag in tags:
    most_view = topic_count(tag)
    most_view_dict = most_view["most_view"]
    pos = str(pos)
    if pos in most_view_dict.keys():
      most_view_dict[pos] = view
    else:
      view_list = []
      for key in most_view_dict.keys():
        view_list.insert(0,{"key":key , "view":most_view_dict[key]})

      #print(view_list)
      change = None
      for i in range(len(view_list)):
        if view > view_list[i]["view"]:
          change = view_list[i]["key"]

      if change != None:
        #print(change)
        del most_view_dict[change]
        most_view_dict[pos] = view

    most_view["most_view"] = most_view_dict
    update_topic_count(tag,most_view)

    #print(most_view)

##################################################load page
def load_page(page_number:int):
  start_time = time.time()
  page_number = page_number
  count = topic_count("count")
  number_of_news = count["value"]

  all_list = []

  ######## post list
  pos_start = number_of_news - 17 * (page_number)
  if pos_start < 1:
    pos_start = 1
  pos_end = number_of_news - 17 * (page_number - 1)

  post_list = []
  for i in range(pos_start,pos_end+1):
    post_list.append(i)

  all_list.extend(post_list)

  #############hot list 
  hot = topic_count("hot")
  #print(hot)
  number_of_hot = hot["value"]
  pos_start = number_of_hot - 3 * (page_number)
  pos_end = number_of_hot - 3 * (page_number - 1)
  hot_list = []
  length = len(hot["position"])
  if pos_start <= 0:
    print("hot <=0")
    hot_list.insert(0,hot["position"][length-1])
    hot_list.insert(0,hot["position"][length-2])
    hot_list.insert(0,hot["position"][length-3])
  else:
    for i in range(length - pos_end, length - pos_start):
      hot_list.append(hot["position"][i])

  all_list.extend(hot_list)

  ################most view list
  most_view = count["most_view"]
  most_view_list = []
  for key in most_view.keys():
    most_view_list.append(key)

  for i in range(len(most_view_list)):
    most_view_list[i] = int(most_view_list[i])
  
  all_list.extend(most_view_list)

  ############most rate list |none

  ########### find and result
  all_list = find_pos(all_list)
  all_list.sort(key=lambda element: element["position"],reverse=True)

  tam1 = []
  tam2 = []
  tam3 = []
  for i in range(len(all_list)):
    if all_list[i]["position"] in post_list:
      tam1.append(all_list[i])
    if all_list[i]["position"] in hot_list:
      tam2.append(all_list[i])
    if all_list[i]["position"] in most_view_list:
      tam3.append(all_list[i])

  print('Total all time load page elapsed: %.6f seconds' % (time.time() - start_time))


  return (tam1,tam2,tam3)

#######load topic
def load_topic(topic:str,page_number:int):
  start_time = time.time()
  page_number = page_number
  post = topic_count(topic)
  all_list = []

  # post list
  number_of_news = post["value"]
  pos_start = number_of_news - 17 * (page_number)
  if pos_start < 1:
    pos_start = 1
  pos_end = number_of_news - 17 * (page_number - 1)
  post_list = []
  if pos_start <= 0:
    length = len(post["position"])
    post_list.insert(0,post["position"][length-1])
    post_list.insert(0,post["position"][length-2])
    post_list.insert(0,post["position"][length-3])
  else:
    for i in range(pos_start,pos_end+1):
      post_list.insert(0,post["position"][i-1])

  all_list.extend(post_list)

  #most view list
  most_view = post["most_view"]
  most_view_list = []
  for key in most_view.keys():
    most_view_list.append(key)

  for i in range(len(most_view_list)):
    most_view_list[i] = int(most_view_list[i])
  all_list.extend(most_view_list)

  all_list = find_pos(all_list)
  all_list.sort(key=lambda element: element["position"],reverse=True)

  tam1 = []
  tam2 = []
  for i in range(len(all_list)):
    if all_list[i]["position"] in post_list:
      tam1.append(all_list[i])
    if all_list[i]["position"] in most_view_list:
      tam2.append(all_list[i])

  end_time = time.time()
  print('Total all time elapsed: %.6f seconds' % (end_time - start_time))

  return (tam1,tam2)