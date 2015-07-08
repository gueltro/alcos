from alcos import *

##The face is the part of your identity that everyone can see (as the name suggests)
##It is composed of your public key and the list of all the alcos that you have exchanged
##in the past. 

##You can think of this as a log that defines your credibility, in the sense that you may 
##convince someone that you are reliable by showing them the story of your past transactions
##in which you have behaved honestly.

##You may also store  dishonest alcos on the face (if you want). For example you may
##store some transactions in which you behaved honestly but someone else behaved dishonestly. 
##You may also store alcos in which you behaved dishonestly, (you may have double spent
##or issued an alcos that you failed to fulfill. 
##It may seem that it is never convenient to show your own dishonest actions, but it may be
##sometimes, for example if you suspect that the other party may discover of your past
##misbehaviour anyway.

class Face():
    
    def __init__(self, public_key):
        self.public_key = public_key
        self.past = []

    def get_alcos_from_name(self,alcos_name):
        possible_alcos = [alcos for alcos in self.get_past() if alcos.name == alcos_name]
        
        alcos = None
        
        if len(possible_alcos) == 1:
            alcos = possible_alcos[0]
        
        if len(possible_alcos) > 1:
            print  "There are multiple alcos with name " + alcos_name
            print   "The oldest one will be returned, but this behaviour is dangerous."
            alcos = possible_alcos[0]
        return alcos   

    ##Insert a new contract to this public identity
    def add_to_past(self,alcos):
        if isinstance(alcos,Alcos):
            ##Create a function for this situation
	    old_alcos = self.get_alcos_from_name(alcos.name)   
	    
	    if old_alcos != None:
	        old_transactions = old_alcos.transactions
        	new_transactions = alcos.transactions
            	assert old_transactions == new_transactions[:len(old_transactions)],\
                    "Duplicate alcos without common history. Alcos forking must have happened"
            self.past.append(alcos)
        else:
            print "The object " + str(alcos) +" is not an alcos. Nothing happens."

    def get_past(self):
	    return self.past


    ##Check if all of the alcos in your transactions are valid alcos in which
    ## all the involved parties behaved honestly
    def is_face_clean(self):
        for alcos in self.get_past():
            if not alcos.check_integrity():
                return False
        return True

    ##Put the second signature on an alcos that was offered you from the owner
    def accept(self,receiver_private_key):
        last_transaction = self.transactions[-1]
        last_transaction.accept_offered_transaction(receiver_private_key)   

    def is_offered():
        last_transaction = self.transactions[-1]
        return last_transaction.is_offer()

    ##Store this publicidentity as a pickle file at path
    def to_file(path):
        store(self, path)
    
    ##Obtain a string that can be used to represent this publicidentity
    def to_string(self):
       object_to_string(self) 
