import hashlib
from interactive_setup import *
from gpg_utils import *
from storage_utils import *

def hash(string):
    return hashlib.sha224(string).hexdigest() 
