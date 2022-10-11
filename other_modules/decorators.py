import time

def count_run_time(func):
    name = ""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        return_value = func(*args, **kwargs)
        print('Total time '+name+' process: %.6f seconds' % (time.time() - start_time))
        return return_value
    return wrapper

