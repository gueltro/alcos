from face import *

##A wallet is an abstraction that collect your personal information.
##It stores all of the PGP public keys that you interacted with and
##it stores your face, that is the history of all of the alcos that 
##you interacted with.

##User should have full control of the wallet, in the sense that they 
##should be able to interact with the underlying alcos and keys, 
##possibly deleting information.

class Wallet():

    def __init__(self, gpg, key_id):
        ##Setup GPG identity
        self.gpg = gpg
        self.key_id = key_id
        self.face = Face(public_key)  

	
    ##Store this alcos as a pickle file at wallet
    def to_file(path):
        store(self, path)
    
    ##Obtain a string that can be used to represent this wallet
    def to_string(self):
       object_to_string(self) 

