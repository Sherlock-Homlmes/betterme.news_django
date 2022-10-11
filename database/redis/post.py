from .main import r
from ..mongodb.main import tdtb
from ..mongodb.main import take_ndb
from other_modules.decorators import count_run_time
from other_modules.feature_func import str_to_dict

def topic_count(key):
    result = r.get(key)
    print(result)
    if result:
        return str_to_dict(result)
    else:
        result = tdtb.find_one( { 'name': key } )
        del result["_id"]
        r.set(key,str(result))
        r.expire(name=key, time=300)
        return result

class MinimumPost:

    def __new__(self,value):
        if type(value) == int:
            self.minimum_post = r.hgetall("m"+str(value))
        elif type(value) == dict:
            self.minimum_post = r.hgetall("m"+str(value["position"]))
        else:
            print("value not valid")
            return None

        if self.minimum_post == {}:
            return None
        else:
            return self.minimum_post

    @staticmethod
    def set_minimum_post(obj:dict):
        del obj["_id"]
        key = "m"+str(obj["position"])
        r.hmset(key,obj)
        r.expire(name=key, time=86400)

class MultiMinimumPost:

    def __new__(self,post_pos_list:list):
        post_list = []
        get_list = []

        for post_pos in post_pos_list:
            result = MinimumPost(post_pos)
            if result:
                result["position"] = int(result["position"])
                get_list.append(result["position"])
                post_list.append(result)

        new_list = list(filter(lambda v: v not in get_list,post_pos_list))

        return (new_list,post_list)

    @staticmethod
    def set_multi_minimum_post(post_list:list):
        for post in post_list:
            result = MinimumPost(post)
            if result == None:
                MinimumPost.set_minimum_post(post)

class PostContent:
    @count_run_time
    def __new__(self,name:str):
        result = r.get(name)
        if result:
            return str_to_dict(result)
        else:
            result = take_ndb("name",name)
            if result == False:
                return False
            else:
                del result["_id"]
                r.set(name,str(result))
                r.expire(name, time=86400)
                return result
