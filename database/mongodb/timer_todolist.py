from .main import tt_db

#start
#########################################database#####################################

def create_todo_timer(user_id):
    data = {
        "user_id":user_id,

        "pomodoro_count":0,
        "total_time":0,
        "pomodoro_study":25,
        "pomodoro_break":5,

        "todolist":[],
    }

    tt_db.insert_one(data)

    return data

def take_todo_timer(user_id) -> list:
    element = tt_db.find_one( { 'user_id': user_id } )
    if element:
        return element
    else:
        return create_todo_timer(user_id)


#to do
def new_todo(user_id,task_name):
    element = take_todo_timer(user_id)
    if task_name not in element:
        element["todolist"].append(task_name)

    tt_db.update_one({"user_id":user_id},{'$set':element})

def del_todo(user_id,task_name):
    element = take_todo_timer(user_id)
    element["todolist"].remove(task_name)

    tt_db.update_one({"user_id":user_id},{'$set':element})

#timer
def pomodoro_timer(user_id,pomodoro_study:int,pomodoro_break:int):
    element = take_todo_timer(user_id)
    element['pomodoro_study'] = pomodoro_study
    element['pomodoro_break'] = pomodoro_break

    tt_db.update_one({"user_id":user_id},{'$set':element})
    
def add_timer(user_id):
    element = take_todo_timer(user_id)
    element["pomodoro_count"] += 1
    element["total_time"] += element["pomodoro_study"]

    tt_db.update_one({"user_id":user_id},{'$set':element})


