from .main import chat_db

def add_chat(data):
    chat_db.insert_one(data)

def find_chat(last_message:int) -> list:
    pos_list = [*range(last_message-30,last_message,1)]
    element = chat_db.find({"id": { '$in': pos_list }  })
    value = []
    for ele in element:
        del ele["_id"]
        value.append(ele)
    return value