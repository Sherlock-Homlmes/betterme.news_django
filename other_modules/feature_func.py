
#string to dict
import ast
def str_to_dict(value):
	return ast.literal_eval(value)

#auto generate random string
import random
import string

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

