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



##A signer can use this to sign a message with his
##GPG key
def sign(message, signer_id, signer_gpg):
    signed_data = signer_gpg.sign(message)
    print message + " signed with my private key: " + private_key
    return signed_data
    


def verify(promise, promise_signature, verifier_gpg, original_owner):
    print "---"
    print promise
    print promise_signature
    print original_owner
    return verifier_gpg.verify(promise_signature)

