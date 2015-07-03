import gnupg
from os.path import expanduser

def gpg_setup(home = expanduser("~") + "/.alcos" ):
    gpg = gnupg.GPG(gnupghome=home)
    gpg.encoding = 'utf-8'
    return gpg

##Import new gpg_keys
def import_gpg_keys_from_string(gpg,data):
    gpg.import_keys(data)

##Interactivley create a gpg_identity
def create_gpg_keys(gpg, params):
   key_params = gpg.gen_key_input(**params) 
#    key_params = gpg.gen_key_input(name_real="giulio", key_type="RSA", key_length=1024)
   gpg.gen_key(key_params)

##A signer can use this to sign a message with his
##GPG key
def sign(message, signer_id, signer_gpg):
    signed_data = signer_gpg.sign(message,keyid = signer_id)
    print message + " signed with my identity: " + signer_id  
    return signed_data
    
def verify(message, message_signature,  signer_public_key):
    ##Temporary gpg profile used to verify without needing an identity 
    temp_gpg = gpg_setup("/tmp/" + str(hash(signer_public_key)))
    import_gpg_keys_from_string(temp_gpg,signer_public_key)
    signer_fingerprint = temp_gpg.list_keys()[0]["fingerprint"]

    is_valid_signature =  temp_gpg.verify(message_signature.data)
    signature_fingerprint = is_valid_signature.fingerprint

    if is_valid_signature and (signature_fingerprint == signer_fingerprint):
        print "Signature for following promise was correct: "
        print message
        return True
    else:
        print "Signature for following promise was compromised: "
        print message
        return False

##Utils for interactive setup. Maybe in the future this will be done with the cli-interface
def gpg_interactive_setup():
    print "Welcome to the interactive gpg setup! Do you want to create a new PGP key-pair, or do you want to import one?"
    user_input = "n"
    while (user_input != "I") and (user_input!= "N"):
        user_input = raw_input("N = New key-pair, I = Import an existing key-pair:   ") 
 
    gpg = gpg_setup()      
    if (user_input == "N"):
        keys_interactive_setup(gpg)
    
    return gpg

##Create a new PGP key from user input
def keys_interactive_setup(new_gpg):
    name_real = ""
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
