from utils import *

class Transaction():

    def __init__(self,alcos_name,sender_public_key,receiver_public_key):
        self.alcos_name = alcos_name
        self.sender_public_key = sender_public_key
        self.receiver_public_key = receiver_public_key
        self.sinthesis = alcos_name + "|" + hash(sender_public_key) + "|" + hash(receiver_public_key)
        self.sender_signature = None
        self.receiver_signature = None


    ##Utils to propose a transaction to someone, and for that someone to accept 
    def offer_transaction(self, sender_private_key):
        self.sender_signature = sign(self.sinthesis, sender_private_key)

    def accept_offered_transaction(self,receiver_private_key):
        if self.sender_signature != None:
            print "This transaction was not proposed by anyone. Nothing happens"
        if verify(self.sinthesis, self.sender_signature,self.sender_public_key):
            self.receiver_signature = sign(self.sinthesis, receiver_private_key)
        else:
            print "This transaction was not signed correctly. Nothing happens"

    ##Check if the transaction is an offer, by making sure
    ##that the sender signed but the receiver di not
    def is_offer():
        if (self.sender_signature != None) and (self.receiver_signature == None):
            return True
        return False

    ##Utils to request a transaction from someone, and for that someone to accept 
    ##(Not used yet, but it will be useful in the future)    
    def request_transaction(receiver_private_key):
        self.receiver_signature = sign(self.sinthesis, receiver_private_key)

    def accept_requested_transaction(sender_private_key):
        if self.sender_signature != None:
            print "This transaction was not proposed by anyone. Nothing happens"
        if verify(self.sinthesis, self.sender_signature,self.sender_public_key):
            self.receiver_signature = sign(self.sinthesis, receiver_public_key)
        else:
            print "This transaction was not signed correctly. Nothing happens"

    
