import gnupg
from os.path import expanduser

gpg_debug = 0

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
    temp_gpg = gpg_setup("/tmp/" + str(hash(str(signer_public_key) + str(message))))
    import_gpg_keys_from_string(temp_gpg,signer_public_key)
    signer_fingerprint = temp_gpg.list_keys()[0]["fingerprint"]
    
    if message_signature == None:
        return False

    is_valid_signature =  temp_gpg.verify(message_signature.data)
    signature_fingerprint = is_valid_signature.fingerprint
    
    if is_valid_signature and (signature_fingerprint == signer_fingerprint):
        if gpg_debug:
            print "Signature for following promise was correct: "
            print message
        return True
    else:
        print "Signature for following promise was compromised: "
        print message
        return False

def get_gpg_fingerprint_from_public_key(public_key):
    temp_gpg = gpg_setup("/tmp/" + str(hash(public_key)))
    import_result = temp_gpg.import_keys(public_key)
    fingerprint = import_result.fingerprints
    return fingerprint

def get_uid_from_public_key(public_key):
    temp_gpg = gpg_setup("/tmp/" + str(hash(public_key)))
    import_result = temp_gpg.import_keys(public_key)
    uid = temp_gpg.list_keys()[0]["uids"][0] ##dark magic to change
    return uid

