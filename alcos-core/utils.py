import hashlib
import time
import os.path
from interactive_setup import *
from gpg_utils import *
from storage_utils import *



def hash(string):
    return hashlib.sha224(string).hexdigest() 

def get_current_time():
    return time.strftime("%c")
