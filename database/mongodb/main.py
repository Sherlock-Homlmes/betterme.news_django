from database import dtbs

dtb = dtbs['news_data']

tdtb = dtbs["topic_position"]
ldtb = dtbs["load_news_data"]
rac_db = dtbs['rating_and_comment']

user_db = dtbs['user_info']
ana_db = dtbs['user_analyze']

tt_db = dtbs['timer_todo']

chat_db = dtbs["chat"]

#take_data
def take_ndb(key,value):
  tests = dtb.find_one( { '{}'.format(key): value } )
  if tests:
    return tests 
  else: 
    return False