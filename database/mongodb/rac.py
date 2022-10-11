from .discord_user import take_discord_user_by_id_list

from .main import rac_db

#start
#########################################database#####################################
#cre_data
async def creRAC(user_id:int,position:int,rate:int,comment:str,comment_number:int):

  if check_can_comment(user_id,position) == False:
    return False
  else:
    rac = {
    "user_id": user_id,

    "position":position,

    "rate":rate,
    "comment":comment,
    "comment_number":comment_number
    }
    rac_db.insert_one(rac)

    return True

#take_data
def takeRAC(key,value) -> list:
  element = rac_db.find( { f'{key}': value } )
  value = []

  #take all element
  for ele in element:
    value.append(ele)

  #take all user
  user_list = []
  for val in value:
    user_list.append(val['user_id'])

  user_dict = take_discord_user_by_id_list(user_list)

  #sort element and process infomation
  for i in range(len(value)):
    value[i]['avatar_url'] = user_dict[ str(value[i]['user_id']) ] ['avatar_url']
    value[i]['username'] =   user_dict[ str(value[i]['user_id']) ] ['username']

  return value

async def take_rate_number_by_pos(position):
  value = rac_db.find( { 'position': position } ).sort('comment_number',-1).limit(1)

  for v in value:
    return v['comment_number']

#check if can comment
def check_can_comment(user_id:int,position:int):
  can_cmt = rac_db.count_documents(
    {
    "position":position,
    "user_id":user_id
    }
  )
  if can_cmt >= 1:
    return False
  else:
   return True