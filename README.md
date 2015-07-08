# alcos
Make a cryptographyc promise to your friends and peers.

This is a python wrapper for pgp, that allows people to make promises and sign them with their PGP keys.

For example, if I want to promise to my friend steven that I will give him a beer, I can do the following: 

```
alcos-cli iou -p "1 Beer" steven  -o beer-alcos.txt
```

and this will create a binding contract signed with your PGP identity. Steven can accept the alcos as following:

```
alcos accept beer-alcos.txt 
```

```
Usage:
  alcos-cli.py iou [-p promise] <receiver> [-o output_file] 
  alcos-cli.py promise [-p promise-string] [-i promise-file] [-o output-file]
  alcos-cli.py offer <alcos>  <receiver>  [-o output-file]
  alcos-cli.py accept <alcos> 
  alcos-cli.py export [<object>] <output-file>
  alcos-cli.py import <input-file>
  alcos-cli.py show (issued_promises | owed_promises | past | keys | public_key | private_key | <object>) 

Options:
  -h --help     Show this screen.
  -p specify promise from a string
  -i specify promise from an input file
  -o output-file      
  --quiet      print less text
  --verbose    print more text
"""
```


-- Work in progress -- 


Usefull manual for gpg 

https://www.gnupg.org/gph/en/manual/c14.html

python gnupg documentation:


https://pythonhosted.org/python-gnupg/



My PGP key:


-----BEGIN PGP PUBLIC KEY BLOCK-----
Version: GnuPG v1

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
vCHb
=BQED
-----END PGP PUBLIC KEY BLOCK-----
