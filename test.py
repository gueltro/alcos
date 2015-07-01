from alcos import *

creator_public_key = "giulio"
creator_private_key = "gueltrini"
promise = "I will give a beer to the owner of this alcos"
promise_signature = sign(promise,creator_private_key)

alcos = Alcos(promise,promise_signature,creator_public_key)
print "---"
print "Test internal alcos variable"
print alcos.name
print alcos.promise
print alcos.promise_signature
print alcos.creator_public_key
print alcos.transactions  

receiver_public_key = "steven"
receiver_private_key = "rigsby"

print "---"
print "test first offer"

print alcos.name +"|"+ hash("giulio") +"|"+ hash("steven")

alcos.offer(creator_private_key,receiver_public_key)

print alcos.transactions

offer_transaction = alcos.transactions[0]
print offer_transaction.alcos_name
print offer_transaction.sender_public_key
print offer_transaction.receiver_public_key
print offer_transaction.sinthesis
print offer_transaction.sender_signature
print offer_transaction.receiver_signature

print "---"
print "Test acceptance protocol"
alcos.accept(receiver_private_key)

print "Test received transaction"

offer_transaction = alcos.transactions[0]
print offer_transaction.alcos_name
print offer_transaction.sender_public_key
print offer_transaction.receiver_public_key
print offer_transaction.sinthesis
print offer_transaction.sender_signature
print offer_transaction.receiver_signature


