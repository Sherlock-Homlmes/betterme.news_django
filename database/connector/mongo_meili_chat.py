from ..mongodb.chat import find_chat,add_chat
from ..mongodb.discord_user import take_discord_user_by_id_list
from ..meilisearch.chat import employee_chat_index

all_chat = [
    "admin",
    "modder",
    "designer",
    "developer"
]

import json
#from pymongo import json_util
#def parse_json(data):
#    return json.loads(json_util.dumps(data))

def add_employee_chat(chat_element):
    message_id = employee_chat_index.get_stats()["numberOfDocuments"] + 1

    documents = [
        {
            "id": message_id,
            "user_id": chat_element["user_id"],
            "message" : chat_element["message"],
            "time_stamp" : chat_element["time_stamp"],
        }
    ]

    add_chat(documents[0])
    del documents[0]["_id"]
    employee_chat_index.add_documents(documents)

def full_chat_data(last_message:int):

    data = find_chat(last_message)
    user_id_list = None
    user_id_list = []
    result = {}

    for dat in data:
        if dat["user_id"] not in user_id_list:
            user_id_list.append(dat["user_id"])
    user_list = take_discord_user_by_id_list(user_id_list)

    for dat in data:
        user = user_list[str(dat["user_id"])]
        dat["username"] = user["username"]
        dat["avatar_url"] = user["avatar_url"]
        result[str(dat["id"])] = dat
        del result[str(dat["id"])]["id"]
    print(result)
    
    return result