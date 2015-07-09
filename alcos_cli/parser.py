#Generic parser used to get an input from command line and transform it into a python object
import os
from wallet import *

class Parser():
    
    def parse(self, wallet, target_object):
        return self.generic_object_parse(wallet, target_object)

    ##First level generic parsing
    def generic_object_parse(self, wallet, target_object):
        ##If the object is a file, load it and then re_parse it 
        if os.path.isfile(str(target_object)):
            return self.generic_object_parse(wallet,load(target_object))

        if isinstance(target_object, object):
            return self.parse_object(wallet, target_object)  

    def parse_object(self, wallet, target_object):
        ##Show a python object
        if isinstance(target_object, Alcos):
            return target_object 

        if isinstance(target_object, Wallet):
            return target_object 

        if isinstance(target_object, Face):
            return target_object
        
        ##get an object from hash
        if isinstance(target_object, str):
            target_string = target_object
            return self.parse_string(wallet,target_string)

    def parse_string(self, wallet, target_string): 
    	maybe_alcos = wallet.get_alcos_from_name(target_string) 
    	if isinstance(maybe_alcos, Alcos):
            return maybe_alcos
        return None
