import pickle
from utils import *

class Alcos():

    def  __init__(self, promise, promise_signature, creator_public_key):
            self.name =  hash(promise)
            self.promise = promise
            self.promise_signature = promise_signature
            self.creator_public_key = creator_public_key
            self.transactions = []
 
    def get_owner_public_key(self):
        ##If no transaction ever happened then the creator
        ##of the alcos is the owner
        if len(self.transaction) == 0:
            return self.creator_public_key
        ##If a transaction happen, the receiver of the
        ##last transaction is the owner:
        else:
            last_transaction = self.transactions[-1]
            return last_transaction.receiver_public_key
    
    ##Check that all of the transaction since the creation of
    ##the alcos are correctly signed
    def check_integrity(self):
        ##Check that the advertised owner created the alcos
        original_owner = self.creator_public_key
        if verify(self.promise,self.promise_signature,original_owner):
            self.recursive_check(original_owner,0)
        else:
            print "The advertised owner did not create the file"
            return False

    def recursive_check(old_owner, checked_transactions):
        ##We checked all of the transactions, and the alcos is valid
        if len(self.transactions) == checked_transactions:
            print "The alcos is valid"
            return True

        this_transaction = self.transactions[checked_transactions]
        this_sinthesis = this_transaction.sinthesis 
        this_sender = this_transaction.sender_public_key
        this_receiver = this_transaction.receiver_public_key
        this_sender_signature = this_transaction.sender_signature
        this_receiver_signature = this_transaction.receiver_signature

        if this_sender != old_owner:
            print "Transaction " + this_transaction.sinthesis + " have an invaild sender"
            return false

        if not verify(this_sinthesis,this_sender_signature,this_sender):
            print "Transaction " + this_transaction.sinthesis + " have an invaild signature from the sender"
            return false

        if not verify(this_sinthesis,this_receiver_signature,this_receiver):
            print "Transaction " + this_transaction.sinthesis + " have an invaild signature from the receiver"
            return false
        
        new_owner = this_receiver
        return self.recursive_check(new_owner, checked_transactions + 1)



class Transaction():

    def __init(self,alcos_name,sender_public_key,receiver_public_key):
        self.alcos_name = alcos_name
        self.sender_public_key = sender_public_key
        self.receiver_public_key = receiver_public_key
        self.sinthesis = alcos_name + "|" + hash(sender_public_key) + "|" + hash(receiver_public_key)
        self.sender_signature = None
        self.receiver_signature = None


    ##Utils to propose a transaction to someone, and for that someone to accept 
    def propose_transaction(sender_private_key):
        self.sender_signature = sign(self.sinthesis, sender_public_key)

    def accept_proposed_transaction(receiver_private_key):
        if self.sender_signature != None:
            print "This transaction was not proposed by anyone. Nothing happens"
        if verify(self.tag, self.sender_signature,self.sender_public_key):
            self.receiver_signature = sign(self.sinthesis, receiver_private_key)
        else:
            print "This transaction was not signed correctly. Nothing happens"

    ##Utils to request a transaction from someone, and for that someone to accpet 
    def request_transaction(receiver_private_key):
        self.receiver_signature = sign(self.sinthesis, receiver_private_key)

    def accept_requested_transaction(sender_private_key):
        if self.sender_signature != None:
            print "This transaction was not proposed by anyone. Nothing happens"
        if verify(self.tag, self.sender_signature,self.sender_public_key):
            self.receiver_signature = sign(self.sinthesis, receiver_public_key)
        else:
            print "This transaction was not signed correctly. Nothing happens"

    
