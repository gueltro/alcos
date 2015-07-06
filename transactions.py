from utils import *

class Transaction():

    def __init__(self,alcos_name,sender_fingerprint,receiver_fingerprint):
        self.alcos_name= alcos_name
        ##Fingerprints for sender and receiver
        self.sender_fingerprint = sender_fingerprint
        self.receiver_fingerprint = receiver_fingerprint
        #The synthesis is built as the hash of the alcos name and the 
        self.sinthesis = hash(str(alcos_name) + str(sender_fingerprint) + str(receiver_fingerprint))
        self.sender_signature = None
        self.receiver_signature = None


    ##Utils to propose a transaction to someone, and for that someone to accept 
    def offer_transaction(self, sender_id, sender_gpg):
        self.sender_signature = sign(self.sinthesis, sender_id, sender_gpg)

    def accept_offered_transaction(self, receiver_id, receiver_gpg):
        assert self.sender_signature != None ,\
            "Null transaction detected."
        assert verify(self.sinthesis, self.sender_signature, self.sender_fingerprint) ,\
             "This transaction was not signed correctly. Nothing happens"

        self.receiver_signature = sign(self.sinthesis, receiver_id, receiver_gpg)

    ##Check if the transaction is an offer, by making sure
    ##that the sender signed but the receiver did not
    def is_valid_offer(self):
        if (self.sender_signature != None) and (self.receiver_signature == None):
            if verify(self.sinthesis, self.sender_signature, self.sender_fingerprint):
                return True
        return False

   
