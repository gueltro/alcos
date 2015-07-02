import gnupg
from os.path import expanduser


def gpg_setup():
    home = expanduser("~")
    gpg = gnupg.GPG(gnupghome=home)
    gpg.encoding = 'utf-8'
    return gpg


    input_data = gpg.gen_key_input(key_type="RSA", key_length=1024)
    key = gpg.gen_key(input_data)
    ascii_armored_public_keys = gpg.export_keys(keyids)

setup()




def sign(message,private_key):
    print message + " signed with my private key: "+private_key
    return  message + " signed with my private key: "+private_key    


def verify(promise, promise_signature, original_owner):
    print "---"
    print promise_signature
    print "The promise " + promise + " was signed by " +  original_owner 
    return True
