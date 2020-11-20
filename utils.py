from datetime import datetime
import threading
import random
import string

def execute_callback(callback, args=()):
    if not callback == None:
        return callback(*args)


def log(*args):
    print(datetime.now().strftime("[%H:%M:%S %d-%m-%Y]"), "["+threading.current_thread().getName()+"]", *args)


def get_random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))
