import gnupg
from os.path import expanduser


def setup():
    home = expanduser("~")
    gpg = gnupg.GPG(gnupghome=home)
    gpg.encoding = 'utf-8'
    return gpg


    input_data = gpg.gen_key_input(key_type="RSA", key_length=1024)
    key = gpg.gen_key(input_data)
    ascii_armored_public_keys = gpg.export_keys(keyids)

setup()
