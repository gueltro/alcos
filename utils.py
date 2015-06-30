import haslib

def hash(string):
    return hashlib.sha224(string).hexdigest() 
