from face import *

##A wallet is an abstraction that collect your personal information.
##It stores all of the PGP public keys that you interacted with and
##it stores your face, that is the history of all of the alcos that 
##you interacted with.

##User should have full control of the wallet, in the sense that they 
##should be able to interact with the underlying alcos and keys, 
##possibly deleting or altering information. The protocol should be 
##sound because of cryptography, and not because of obscurity.

class Wallet():

    def __init__(self, gpg, my_key_id):
        ##Setup GPG identity
        self.gpg = gpg
        self.key_id = my_key_id
        self.face = Face(self.get_public_key(my_key_id))  

    ##Hooks to GPG identity
    
    ##return GPG public key in armored ASCII
    def get_public_key(self, key_id):
        return self.gpg.export_keys(key_id, False) #False means public

    ##return GPG public key in armored ASCII
    def get_private_key(self, key_id):
        return self.gpg.export_keys(key_id, True) #False means public
    
    ##Get the keys of the owner of the wallet
    def get_my_public_key(self):
        return self.get_public_key(self.key_id)
    
    def get_my_private_key(self):
        return self.get_private_key(self.key_id)

    def import_keys_from_string(self, key_string):
        import_gpg_keys_from_string(self.gpg,key_string)
    
    ##Store alcos in face
    def add_alcos_to_past(self,alcos):
        self.face.add_alcos_to_past(alcos)

    ##Create a new alcos and add it to the wallet.
    def create_alcos(self,promise):
        owner_gpg = self.gpg
        owner_id = self.key_id
        promise_signature = sign(promise, owner_id, owner_gpg)
        owner_public_key = self.get_my_public_key()

        new_alcos = Alcos(promise, promise_signature, owner_public_key)
        self.add_alcos_to_past(new_alcos)

    ##Trading utils to exchange and create alcos

    ##Offer one of the alcos that you own to someone
    ##that you know (using gpg receiver_id). This function
    ##only change the internal representation of the alcos, and 
    ##does not return anything, In order to get a string or a file
    ##with your offer, you should use offer_with_string or 
    ##offer_with file
    def offer_alcos(self,alcos,receiver_public_key):
        past = self.get_past()
        alcos_owner_key = alcos.get_owner_public_key()
        wallet_owner_public_key = self.get_my_public_key() 
        ##TODO add check that receiver is in my known contact

        if (alcos not in past):
            print "alcos " + str(alcos) + "was added to your past"
            self.add_alcos_to_past(alcos)

        if (alcos_owner_key != wallet_owner_public_key):
            print "This alcos is not yours. Nothing will happen"
            return

        if not alcos.check_integrity():
            print "This alcos is corrupt. Nothing will happen." 
            return

        if  (alcos.is_valid_offer()): 
            print "This alcos is already being offered to someone else! Are you trying to double spend?"
            return   
        
        alcos.offer(self.key_id, self.gpg, receiver_public_key)

    def accept_alcos(self, alcos):  

        past = self.get_past()
        last_transaction = alcos.transactions[-1]

        alcos_owner_public_key = alcos.get_owner_public_key()
        wallet_owner_public_key = self.get_my_public_key()
        sender_public_key = last_transaction.sender_public_key
        receiver_key = last_transaction.receiver_public_key


        if (alcos not in past):
            print "alcos " + str(alcos) + "was added to your past"
            self.add_alcos_to_past(alcos)
            

        if  not (alcos.is_valid_offer()): 
            print "This alcos is not a valid offer, nothing happens." 
            return  

        if (alcos_owner_public_key != sender_public_key):
            print "The person that sent you this alcos is not the legitimate owner of this alcos"
            return

        if (wallet_owner_public_key != receiver_key):
            print "This alcos was not sent to you, therefore you can not accept it"
            return

        alcos.accept(self.key_id, self.gpg)

    
    ##Get the list of all past alcos from the face
    def get_past(self):
        return self.face.past

    ##Store this alcos as a pickle file at wallet
    def to_file(self,path):
        store(self, path)
    
    ##Obtain a string that can be used to represent this wallet
    def to_string(self):
       object_to_string(self) 

