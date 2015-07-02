from transactions import *
from utils import *


##An alcos is a just  a cryptographic promise. The creator of the alcos 
##promise that it will give something (dollars, beer, food, stamps..) to
##the owner of the alcos. The owner of the alcos can be changed if the 
##current owner signs a transaction where it declare that he gives the 
##alcos to someone else.


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
        if len(self.transactions) == 0:
            return self.creator_public_key
        ##If a transaction happen, the receiver of the
        ##last transaction is the owner:
        else:
            last_transaction = self.transactions[-1]
            return last_transaction.receiver_public_key
    
    ##Check that all of the transaction since the creation of
    ##the alcos are correctly signed
    def check_integrity(self):
        ##Check that the advertised creator created the alcos
        creator = self.creator_public_key
        if verify(self.promise,self.promise_signature,creator):
            self.recursive_check(creator,0)
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

    ##Used to offer the alcos to someone: create a new transaction and 
    ##sign it as a sender with your private_key. At this point the
    ##transaction is incomplete, (in the sense that possible_transaction.receiver_signature == 0)
    def offer(self, owner_id, owner_gpg, receiver_public_key):
        ##Initialize new transaction
        possible_transaction =  Transaction(self.name, self.get_owner_public_key(), receiver_public_key)
        possible_transaction.offer_transaction(sender_id, sender_gpg) 
        ##Add it to the list of transactions 
        self.transactions.append(possible_transaction)
    
    ##Put the second signature on an alcos that was offered you from the owner
    def accept(self,receiver_id,receiver_gpg):
        last_transaction = self.transactions[-1]
        last_transaction.accept_offered_transaction(receiver_id, receiver_gpg)   
    
    ##Check if this alcos is offered to someone
    def is_offered():
        last_transaction = self.transactions[-1]
        return last_transaction.is_offer()

    ##Store this alcos as a pickle file at path
    def to_file(path):
        store(self, path)
    
    ##Obtain a string that can be used to represent this alcos
    def to_string(self):
       object_to_string(self) 

