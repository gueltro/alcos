from transactions import *


# An alcos is a just  a cryptographic promise. The creator of the alcos
# promise that it will give something (dollars, beer, food, stamps..) to
# the owner of the alcos. The owner of the alcos can be changed if the
# current owner signs a transaction where it declare that he gives the
# alcos to someone else.

# This creates a chain of trust from the orignal issuer of the alcos
# to all of the people that use that alcos as a means of exchange.


class Alcos():

    def __init__(self, promise, promise_signature, creator_public_key):
            self.name = hash(promise)
            self.timestamp = get_current_time()
            self.promise = promise
            self.promise_signature = promise_signature
            self.creator_public_key = creator_public_key
            self.transactions = []

    # return the owner of the alcos at final_transaction
    # where final_transaction is an integer that represents
    # the position of the last transaction 

    def get_owner_public_key(self, final_transaction=None):

        if final_transaction is None:
            final_transaction = len(self.transactions)

        assert (0 <= final_transaction) and (final_transaction <= len(self.transactions)),\
            "The time of the ownership is out of range. No owner at that time"

        if final_transaction == 0:
            return self.creator_public_key

        last_transaction = self.transactions[final_transaction-1]
        return last_transaction.receiver_public_key

    def get_owner_fingerprint(self, final_transaction=None):
        owner_public_key = self.get_owner_public_key()
        owner_fingerprint = get_gpg_fingerprint_from_public_key(owner_public_key)
        return owner_fingerprint

    # Check that all of the transaction since the creation of
    # the alcos, up to final_transaction are correctly signed.
    # final_transaction is an integer that represent the position
    # of the final transaction in self.transactions
    def check_integrity(self, final_transaction = None):
        # Check that the advertised creator created the alcos
        creator_public_key = self.creator_public_key
        # Hack to escape the fact that self can't be referenced in arguments, i.e
        # def check_integrity(self, final_transaction = len(self.transactions)):
        # NameError: name 'self' is not defined (TODO find a cleaner way to do this)
        if final_transaction == None:
            final_transaction = len(self.transactions)
        # Hack to make sure that final_trasaction is in range
        final_transaction = max(0, min(final_transaction,len(self.transactions)))

        if verify(self.promise,self.promise_signature,creator_public_key):
            return self.recursive_check(creator_public_key,0,final_transaction)
        else:
            print "The advertised owner did not create the file"
            return False

    def recursive_check(self, old_owner_public_key, checked_transactions, final_transaction):

        # We checked all of the transactions, and the alcos is valid
        if final_transaction == checked_transactions:
            return True

        # Collect parmether of the transaction
        this_transaction = self.transactions[checked_transactions]
        this_sinthesis = this_transaction.sinthesis
        this_sender_public_key = this_transaction.sender_public_key
        this_receiver_public_key = this_transaction.receiver_public_key
        this_sender_signature = this_transaction.sender_signature
        this_receiver_signature = this_transaction.receiver_signature

        if this_sender_public_key != old_owner_public_key:
            print "Transaction " + this_transaction.sinthesis + " have an invaild sender"
            return False


        if not verify(this_sinthesis,this_sender_signature,this_sender_public_key):
            return False

        if not verify(this_sinthesis,this_receiver_signature,this_receiver_public_key):
            return False
       
        new_owner = this_receiver_public_key
        return self.recursive_check(new_owner, checked_transactions + 1, final_transaction)

    # Used to offer the alcos to someone: create a new transaction and
    # sign it as a sender with your private_key. At this point the
    # transaction is incomplete, (in the sense that possible_transaction.receiver_signature == 0)
    def offer(self, owner_id, owner_gpg, receiver_public_key):
        # Initialize new transaction
        possible_transaction =  Transaction(self.name, self.get_owner_public_key(), receiver_public_key)
        possible_transaction.offer_transaction(owner_id, owner_gpg)
        # Add it to the list of transactions
        self.transactions.append(possible_transaction)
   
    # Put the second signature on an alcos that was offered you from the owner
    def accept(self,receiver_id,receiver_gpg):
        last_transaction = self.transactions[-1]
        last_transaction.accept_offered_transaction(receiver_id, receiver_gpg)  
   
    # Check if this alcos is offered to someone
    def is_valid_offer(self):
        transaction_length =  len(self.transactions)
        # If this alcos was never involved in any transaction, for sure it was not offered
        if transaction_length == 0:
            return False

        if not self.check_integrity(transaction_length -1):
            print "The history of this alcos is corrupted"
            return False
       
        # Is the person that is offering you the alcos
        # the owner of the alcos?
        if transaction_length == 1:
            owner = self.creator_public_key
            sender = self.transactions[0].sender_public_key
            if not owner == sender:
                return False

        if transaction_length > 1:
            last_receiver = self.get_owner_public_key(transaction_length - 1)
            last_sender = self.transactions[transaction_length - 1].sender_public_key
       
            if not  last_receiver == last_sender:
                return False
       
        last_transaction = self.transactions[-1]
        return last_transaction.is_valid_offer()
   
    def pretty_print(self):
        valid_string = "Invalid "
        # Collect paramether to print
        creator_public_key = self.creator_public_key
        creator_id  =  get_uid_from_public_key(creator_public_key)
        owner_public_key = self.get_owner_public_key()
        owner_id = get_uid_from_public_key(owner_public_key)
        receiver_public_key = ""
        receiver_id = ""
       
        is_valid = self.check_integrity()
        is_offered = self.is_valid_offer()
       
        # Decide if the alcos is valid or offered
        if is_offered:
            receiver_public_key = self.transactions[-1].receiver_public_key
            receiver_id = get_uid_from_public_key(receiver_public_key) 
       
        if is_valid or is_offered:
            valid_string = "Valid "

        # Print all of the main info about thi alcos
        print ""
        print valid_string + "Alcos " + self.name
        print "Creator: " + creator_id
        print "Owner: " +  owner_id
        if is_offered:
            print "Offered to: " + receiver_id
        print "Date: " + self.timestamp
        print ""
        print "\t" + self.promise
        print ""

    # Store this alcos as a pickle file at path
    def to_file(self,path):
        store(self, path)
   
    # Obtain a string that can be used to represent this alcos
    def to_string(self):
       object_to_string(self)
