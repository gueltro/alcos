import hashlib
from gpg_utils import *

def hash(string):
    return hashlib.sha224(string).hexdigest() 
