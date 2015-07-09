import pickle


##Wrappers for pickle, used to store files in some path
def store(obj,path):
    storage_file = open(path,'wb')
    pickle.dump(obj, storage_file) 

def load(path):
    return pickle.load(open(path,"rb"))


##Not sure why yet but this may be useful for things like pasting an
##alcos into an email, blog or similar
def object_to_string(obj):
    return pickle.dumps(obj)

def string_to_object(string):
    return pickle.loads(string)
