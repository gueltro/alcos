from utils import *

class Transaction():

    def __init__(self,alcos_name,sender_public_key,receiver_public_key):
        self.alcos_name= alcos_name
        self.sender_public_key = sender_public_key
        self.receiver_public_key = receiver_public_key
        self.sinthesis = hash(str(alcos_name) + str(sender_public_key) + str(receiver_public_key))
        self.sender_signature = None
        self.receiver_signature = None


    ##Utils to propose a transaction to someone, and for that someone to accept 
    def offer_transaction(self, sender_id, sender_gpg):
        self.sender_signature = sign(self.sinthesis, sender_id, sender_gpg)

    def accept_offered_transaction(self, receiver_id, receiver_gpg):
        if self.sender_signature == None:
            return
        if verify(self.sinthesis, self.sender_signature, self.sender_public_key):
            self.receiver_signature = sign(self.sinthesis, receiver_id, receiver_gpg)
        else:
            print "This transaction was not signed correctly. Nothing happens"

    ##Check if the transaction is an offer, by making sure
    ##that the sender signed but the receiver did not
    def is_valid_offer(self):
        if (self.sender_signature != None) and (self.receiver_signature == None):
            if verify(self.sinthesis, self.sender_signature, self.sender_public_key):
                return True
        return False

    ##Utils to request a transaction from someone, and for that someone to accept 
    ##(Not used yet, but it will be useful in the future)    
    def request_transaction(self, receiver_id, receiver_gpg):
        self.receiver_signature = sign(self.sinthesis, receiver_id, receiver_pgp)

    def accept_requested_transaction(self, sender_id, sender_gpg):
        if self.sender_signature != None:
            print "This transaction was not proposed by anyone. Nothing happens"
        if verify(self.sinthesis, self.sender_signature, self.sender_public_key):
            self.receiver_signature = sign(self.sinthesis, receiver_public_key)
        else:
            print "This transaction was not signed correctly. Nothing happens"

    
