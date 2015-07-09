from gpg_utils  import *
from wallet import *


##Test to exchange alcos in a small community formed by Giulio, Jad, and Rigsby. 

##Wallet setup
#
gpg = gpg_interactive_setup("giulio")
walletg = Wallet(gpg, "giulio")
walletg.to_file("bank/walletg")

gpg = gpg_interactive_setup("jad")
walletj = Wallet(gpg, "jad")
walletj.to_file("bank/walletj")

gpg = gpg_interactive_setup("rigsby")
walletr = Wallet(gpg, "rigsby")
walletr.to_file("bank/walletr")
#

def line(message = ""):
    print "---"
    print message
    print "---"

print "Welcome to the first virtual community that will do business using alcos!!"

walletj = load("bank/walletj")
walletg = load("bank/walletg")
walletr  = load("bank/walletr")

bank = [walletj, walletg, walletr] 

members =  str(", ".join([member.key_id for member in bank]))
line( "The members of the society are: " + members + ".")

print members + " have been stuck on an island for one year." 

line( "Jad, the great master of chicken, spent most of his time raising the noble birds. After one year of loneliness, Jad started feeling the necessity of intimacy with a female. He realized that he was ready to give up one of his beloved chickens for any kind of lover, even for a goat. ")

line( "Giulio lives in a cave and breed goats. His day are sad, because he remember the smell of the flower that he once loved, and that he could not find in the island.")

line("Rigsby devoted his time to agriculture, and his garden abounds of food and flowers. He spend most of his day lying down and smoking while he watch his garden growing. When Rigsby goes to sleep, his mind is filled with melancholy, because he misses the taste of roasted chicken.")

line("This apparent stall will be magically resolved by the use of alcos.")

jad_public_key = walletj.get_my_public_key()
giulio_public_key = walletg.get_my_public_key()
rigsby_public_key = walletr.get_my_public_key()

walletj.create_alcos("I will give a chicken to the owner of this alcos")
walletg.create_alcos("I will give a goat to the owner of this alcos")
walletr.create_alcos("I will give flower to the owner of this alcos")

alcos_chicken = walletj.get_past()[0]
alcos_goat = walletg.get_past()[0]
alcos_flower = walletr.get_past()[0]

def show_promises():
    for member in bank:
        line()
        member.show_owed_promises()


line("Giulio and Jad trade their Alcos")

##Jad send a chicken-alcos to Giulio
line("jad offers a chicken-alcos to Giulio")
walletj.offer_alcos(alcos_chicken,giulio_public_key)
line("Giulio accept the chicken-alcos from Jad")
walletg.accept_alcos(alcos_chicken)

##Giulio send a goat alcos to jad
line("Giulio offers a goat-alcos to Jad")
walletg.offer_alcos(alcos_goat,jad_public_key)
line("Jad accept the goat alcos from Giulio")
walletj.accept_alcos(alcos_goat)


line("new situation of the promises")

show_promises()

line("Giulio and Rigsby trade alcos")

##Rigsby send a flower-alcos to Giulio
line("Rigsby offers a flower-alcos to giulio")
walletr.offer_alcos(alcos_flower,giulio_public_key)
line("Giulio accept the chicken-alcos from Jad")
walletg.accept_alcos(alcos_flower)

##Giulio send a chicken- alcos to rigsby
line("Giulio offers a chicken-alcos to Rigsby")
walletg.offer_alcos(alcos_chicken,rigsby_public_key)
line("Rigsby accept the chicken alcos from Giulio")
walletr.accept_alcos(alcos_chicken)

show_promises()


print "And everyone lived happy ever after"

