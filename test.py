from gpg_utils  import *
from wallet import *

##Test to create wallet (success)
"""
gpg = gpg_interactive_setup()
wallet = Wallet(gpg, "giulio")
wallet.to_file("walleta")
"""

##test to load wallet (success)
#wallet = load("mywallet")
"""
print wallet.get_my_public_key()
print wallet.get_my_private_key()

##Test to create an alcos (success) 
wallet.create_alcos("I will give a banana to the owner of this alcos")
new_alcos  = wallet.face.past[0]

print new_alcos.name
print new_alcos.promise
print new_alcos.promise_signature
print new_alcos.creator_public_key
print new_alcos.transactions
if verify(new_alcos.promise,new_alcos.promise_signature,wallet.gpg,"ds"):
    print "Verification went ok"
else:
    print "Verification failed horribly"
"""
##Test to offer an alcos (success) 
"""
gpg = gpg_interactive_setup()
wallet = Wallet(gpg, "giulio")
wallet.to_file("walletg")

gpg = gpg_interactive_setup()
wallet = Wallet(gpg, "rigsby")
wallet.to_file("walletr")
"""

"""
walletg = load("walletg")
walletr = load("walletr")

walletg.create_alcos("I will give a beer to the owner of this alcos ")
new_alcos =  walletg.get_past()[-1]
rigsby_public_key = walletr.get_my_public_key()
print ""
print "alcos created"
print ""
walletg.offer_alcos(new_alcos, rigsby_public_key)


offer_transaction =  new_alcos.transactions[0]
e()
print "details about offer transaction"
e()
print offer_transaction.sinthesis
e()
print offer_transaction.sendr_signature
print offer_transaction.receiver_signature



##Test to receive an alcos (success)

print ""
print "Before rigsby acceptinhg"
print ""

walletr.accept_alcos(new_alcos)

alcos_received =  walletr.get_past()[0]

print alcos_received
alcos_received.transactions[-1].sender_signature
alcos_received.transactions[-1].receiver_signature

walletr.to_file("walletr")





gpg = gpg_interactive_setup()
wallet = Wallet(gpg, "jad")
wallet.to_file("walletj")
"""

walletr = load("walletr")
walletg = load("walletg")
walletj = load("walletj")

##Rigsby's point of view 
jad_public_key = walletj.get_my_public_key() 
alcos_offered =  walletr.get_past()[0]
walletr.offer_alcos(alcos_offered, jad_public_key)

##jad's point of view
walletj.accept_alcos(alcos_offered)

print walletj.get_past()[0].get_owner_public_key()
print walletj.get_my_public_key()

