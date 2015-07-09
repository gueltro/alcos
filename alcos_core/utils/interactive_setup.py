from gpg_utils import *
import wallet
import os.path


def get_home_path():
    home_path = expanduser("~") + "/.alcos"
    if not os.path.isdir(home_path):
        os.makedirs(home_path)
    return home_path

def get_wallet_path():
    home_path = get_home_path()
    wallet_path =  home_path + "/wallet.pkl"
    return wallet_path

def check_if_setup():
    home = get_home_path() 
    wallet_file = home + "/wallet.pkl"
    return  os.path.isfile(wallet_file)

def create_wallet():
    name = ""
    while len(name) < 4:
        name = raw_input("Insert an username with more than 4 letters: ")
    try:
        gpg = gpg_interactive_setup(name) 
    except:
        print "gpg setup failed"

    ##Create your new alcos wallet
    my_wallet = wallet.Wallet(gpg, name) 

    ##Store the newly created wallet
    wallet_path = get_wallet_path()   
    my_wallet.to_file(wallet_path)


def gpg_interactive_setup(name = None):
    print "Welcome to the interactive gpg setup! Do you want to create a new PGP key-pair, or do you want to import one?"
    user_input = "n"
    while (user_input != "I") and (user_input!= "N"):
        user_input = raw_input("N = New key-pair, I = Import an existing key-pair:   ") 
 
    gpg = gpg_setup()      
    if (user_input == "N"):
        keys_interactive_setup(gpg, name)
    
    return gpg

##Create a new PGP key from user input
def keys_interactive_setup(new_gpg, name_real = ""):
    while (name_real == ""):
        name_real  = raw_input("Please insert your name (this will be used as a human readable identifier for your PGP identity):  ")
   
    while (name_real == ""):
        name_real  = raw_input("Please insert your name (this will be used as a human readable identifier for your PGP identity):  ")

    ##Prepare a list with all the parameter of the new PGP key
    new_identity = {}
    new_identity['name_real'] = name_real
    new_identity['key_type'] = "RSA"
    new_identity["key_length"] = "1024"
    
    create_gpg_keys(new_gpg, new_identity)
